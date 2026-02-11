from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import FinancialData, Filing10K, Filing10Q, get_db
from edgar import Company, set_identity
from datetime import datetime, date
from typing import List, Dict, Any

router = APIRouter()

# Set SEC identity for edgar library
set_identity("SignalRefinery Admin user@example.com")

def parse_period_label(period_label: str):
    """
    Parse period label like 'FY 2025' or 'Q1 2026' to approximate period end date.

    Args:
        period_label: Period string from EDGAR (e.g., 'FY 2025', 'Q1 2026')

    Returns:
        Approximate period end date as a date object
    """
    import re

    # Match "FY YYYY" pattern for annual periods
    fy_match = re.match(r'FY (\d{4})', period_label)
    if fy_match:
        year = int(fy_match.group(1))
        # Use Dec 31 as fiscal year end (most common)
        return date(year, 12, 31)

    # Match "Q# YYYY" pattern for quarterly periods
    q_match = re.match(r'Q(\d) (\d{4})', period_label)
    if q_match:
        quarter = int(q_match.group(1))
        year = int(q_match.group(2))

        # Standard calendar quarters
        quarter_end_months = {1: 3, 2: 6, 3: 9, 4: 12}
        month = quarter_end_months[quarter]

        # Last day of quarter
        last_day = 31 if month in [3, 12] else 30

        return date(year, month, last_day)

    # Fallback to current date if parsing fails
    return date.today()

def extract_financials_from_company(symbol: str, company_name: str, cik: str):
    """
    Extract real financial statements from EDGAR using the edgar library.
    Retrieves 5 years of annual (10-K) and quarterly (10-Q) data for:
    Income Statement, Balance Sheet, and Cash Flow data.
    """
    try:
        from edgar import Company

        # Create Company instance to get financial data
        company = Company(symbol)

        extracted_data = []

        # ========== EXTRACT ANNUAL DATA (10-K) ==========
        # Request 5 years of annual data
        for statement_type, statement_method in [
            ('income_statement', company.income_statement),
            ('balance_sheet', company.balance_sheet),
            ('cash_flow', company.cash_flow)
        ]:
            try:
                # Get 5 years of annual data
                statement = statement_method(periods=5, period='annual')

                # Iterate over all items with values
                for item in statement.iter_with_values():
                    # Skip abstract items (headers/sections)
                    if item.is_abstract:
                        continue

                    # Iterate over ALL periods (not just first one)
                    if item.values:
                        for period_label, value in item.values.items():
                            if value is not None:
                                try:
                                    value_float = float(value)

                                    # Parse period label to get period_end date
                                    period_end = parse_period_label(period_label)

                                    extracted_data.append({
                                        'statement_type': statement_type,
                                        'metric_name': item.concept,
                                        'metric_label': item.label,
                                        'value': value_float,
                                        'period_label': period_label,
                                        'period_end': period_end,
                                        'filing_type': '10-K',
                                    })
                                except (ValueError, TypeError):
                                    continue
            except Exception as e:
                print(f"Error extracting annual {statement_type}: {str(e)}")

        # ========== EXTRACT QUARTERLY DATA (10-Q) ==========
        # Request 20 quarters (5 years) of quarterly data
        for statement_type, statement_method in [
            ('income_statement', company.income_statement),
            ('balance_sheet', company.balance_sheet),
            ('cash_flow', company.cash_flow)
        ]:
            try:
                # Get 20 quarters of quarterly data
                statement = statement_method(periods=20, period='quarterly')

                # Iterate over all items with values
                for item in statement.iter_with_values():
                    # Skip abstract items
                    if item.is_abstract:
                        continue

                    # Iterate over ALL periods
                    if item.values:
                        for period_label, value in item.values.items():
                            if value is not None:
                                try:
                                    value_float = float(value)

                                    # Parse period label to get period_end date
                                    period_end = parse_period_label(period_label)

                                    extracted_data.append({
                                        'statement_type': statement_type,
                                        'metric_name': item.concept,
                                        'metric_label': item.label,
                                        'value': value_float,
                                        'period_label': period_label,
                                        'period_end': period_end,
                                        'filing_type': '10-Q',
                                    })
                                except (ValueError, TypeError):
                                    continue
            except Exception as e:
                print(f"Error extracting quarterly {statement_type}: {str(e)}")

        if not extracted_data:
            print(f"Warning: No financial data extracted for {symbol}")
            return None

        return extracted_data

    except Exception as e:
        print(f"Error extracting financials: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

@router.post("/financials/extract/{symbol}")
async def extract_and_store_financials(symbol: str, db: Session = Depends(get_db)):
    """
    Extract financial data from latest 10-K/10-Q filing for a given ticker symbol.
    """
    try:
        # Check if filings exist for this symbol
        filings_10k = db.query(Filing10K).filter_by(symbol=symbol).order_by(Filing10K.filing_date.desc()).all()
        filings_10q = db.query(Filing10Q).filter_by(symbol=symbol).order_by(Filing10Q.filing_date.desc()).all()

        if not filings_10k and not filings_10q:
            raise HTTPException(
                status_code=404,
                detail=f"No filings found for {symbol}. Please fetch filings first using /fetch-filings/{symbol}"
            )

        # Get company name and CIK for XBRL extraction
        import edgar as edgar_module
        results = edgar_module.find_company(symbol)

        if not results or len(results) == 0:
            raise HTTPException(status_code=404, detail=f"Company with symbol '{symbol}' not found")

        company = results[0]
        company_name = company.name if hasattr(company, 'name') else str(company)
        cik = str(company.cik) if hasattr(company, 'cik') else str(company._cik)

        # Extract financial data
        financial_data = extract_financials_from_company(symbol, company_name, cik)

        if not financial_data:
            raise HTTPException(status_code=404, detail=f"Could not extract financial data for {symbol}")

        # Validation logging
        print(f"DEBUG: Extracted data summary for {symbol}:")
        print(f"  - Total metrics: {len(financial_data)}")
        if financial_data:
            annual_count = sum(1 for d in financial_data if d['filing_type'] == '10-K')
            quarterly_count = sum(1 for d in financial_data if d['filing_type'] == '10-Q')
            print(f"  - Annual (10-K): {annual_count}")
            print(f"  - Quarterly (10-Q): {quarterly_count}")

            annual_periods = sorted(set(d['period_label'] for d in financial_data if d['filing_type'] == '10-K'))
            quarterly_periods = sorted(set(d['period_label'] for d in financial_data if d['filing_type'] == '10-Q'))
            print(f"  - Annual periods: {annual_periods}")
            print(f"  - Quarterly periods: {quarterly_periods}")

        # Store in database
        metrics_added = 0
        print(f"DEBUG: Starting to store {len(financial_data)} metrics for {symbol}")

        for data_point in financial_data:
            try:
                period_end = data_point['period_end']
                filing_type = data_point['filing_type']

                # Match filing by period to get accurate filing_date
                if filing_type == '10-K':
                    # Find 10-K filing with year matching the period_end
                    filing = db.query(Filing10K).filter(
                        Filing10K.symbol == symbol,
                        Filing10K.year == period_end.year
                    ).order_by(Filing10K.filing_date.desc()).first()

                    if not filing and filings_10k:
                        # Fallback to most recent 10-K if specific year not found
                        filing = filings_10k[0]
                else:  # 10-Q
                    # Find 10-Q filing with year and quarter matching the period_end
                    period_quarter = ((period_end.month - 1) // 3) + 1
                    filing = db.query(Filing10Q).filter(
                        Filing10Q.symbol == symbol,
                        Filing10Q.year == period_end.year,
                        Filing10Q.quarter == period_quarter
                    ).order_by(Filing10Q.filing_date.desc()).first()

                    if not filing and filings_10q:
                        # Fallback to most recent 10-Q if specific quarter not found
                        filing = filings_10q[0]

                if not filing:
                    print(f"WARNING: No filing found for {filing_type} period {period_end}, skipping metric {data_point['metric_name']}")
                    continue

                filing_date = filing.filing_date

                db_financial = FinancialData(
                    symbol=symbol,
                    filing_type=filing_type,
                    filing_date=filing_date,
                    period_end=period_end,
                    period_start=None,
                    statement_type=data_point['statement_type'],
                    metric_name=data_point['metric_name'],
                    metric_label=data_point['metric_label'],
                    value=data_point['value'],
                    unit="USD",
                    extracted_date=datetime.now()
                )

                db.add(db_financial)
                db.commit()
                metrics_added += 1

            except IntegrityError as e:
                db.rollback()
                # Expected behavior - duplicate period/metric combination
                print(f"DEBUG: Skipping duplicate metric: {data_point['metric_name']} for period {data_point.get('period_end', 'unknown')}")
                continue
            except Exception as e:
                db.rollback()
                print(f"Error storing metric {data_point['metric_name']}: {str(e)}")
                continue

        # Get counts
        total_metrics = db.query(FinancialData).filter_by(symbol=symbol).count()
        print(f"DEBUG: Stored {metrics_added} metrics, total in DB: {total_metrics}")

        return {
            "symbol": symbol,
            "company_name": company_name,
            "metrics_added": metrics_added,
            "total_metrics": total_metrics,
            "statements_extracted": ["income_statement", "balance_sheet", "cash_flow"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting financials: {str(e)}")

@router.get("/financials/{symbol}")
async def get_financials(
    symbol: str,
    statement_type: str = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve stored financial data for a given ticker symbol.
    Optionally filter by statement_type: income_statement, balance_sheet, or cash_flow
    """
    try:
        query = db.query(FinancialData).filter_by(symbol=symbol)

        if statement_type:
            query = query.filter_by(statement_type=statement_type)

        financial_data = query.order_by(
            FinancialData.period_end.desc(),
            FinancialData.statement_type,
            FinancialData.metric_name
        ).all()

        if not financial_data:
            raise HTTPException(status_code=404, detail=f"No financial data found for {symbol}")

        # Group by statement type
        result = {}
        for data in financial_data:
            statement = data.statement_type
            if statement not in result:
                result[statement] = []

            result[statement].append({
                "metric_name": data.metric_name,
                "metric_label": data.metric_label,
                "value": data.value,
                "unit": data.unit,
                "period_end": data.period_end.isoformat(),
                "filing_date": data.filing_date.isoformat(),
                "filing_type": data.filing_type
            })

        return {
            "symbol": symbol,
            "total_metrics": len(financial_data),
            "statements": result
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving financials: {str(e)}")

@router.get("/revenue/{symbol}")
async def get_revenue(
    symbol: str,
    filing_type: str = "10-K",
    db: Session = Depends(get_db)
):
    """
    Get revenue data for a given ticker symbol.

    Args:
        symbol: Ticker symbol (e.g., 'AAPL')
        filing_type: '10-K' (annual, default) or '10-Q' (quarterly)

    Returns:
        List of revenue records with period_end date, sorted by period_end descending
    """
    try:
        # Validate filing_type
        if filing_type not in ["10-K", "10-Q"]:
            raise HTTPException(
                status_code=400,
                detail="filing_type must be '10-K' (annual) or '10-Q' (quarterly). Default is '10-K'."
            )

        # Query for revenue metrics from income statement
        # Common revenue metric names in EDGAR filings
        revenue_concepts = [
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "RevenueFromContractWithCustomer",
            "Revenues",
            "TotalRevenues",
            "NetRevenues",
            "OperatingRevenues",
            "SalesRevenue",
        ]

        revenue_data = db.query(FinancialData).filter(
            FinancialData.symbol == symbol,
            FinancialData.filing_type == filing_type,
            FinancialData.statement_type == "income_statement",
            FinancialData.metric_name.in_(revenue_concepts)
        ).order_by(FinancialData.period_end.desc()).all()

        if not revenue_data:
            raise HTTPException(
                status_code=404,
                detail=f"No revenue data found for {symbol} ({filing_type} filings)"
            )

        # Format response
        result = []
        for data in revenue_data:
            result.append({
                "symbol": symbol,
                "filing_type": filing_type,
                "period_end": data.period_end.isoformat(),
                "filing_date": data.filing_date.isoformat(),
                "revenue": data.value,
                "revenue_label": data.metric_label,
                "unit": data.unit
            })

        return {
            "symbol": symbol,
            "filing_type": filing_type,
            "count": len(result),
            "revenue_data": result
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving revenue data: {str(e)}")
