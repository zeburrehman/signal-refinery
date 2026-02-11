from sqlalchemy.orm import Session
from database import Filing10K, Filing10Q
import edgar
from datetime import datetime, date

# Set user agent for edgar library
edgar.set_identity("SignalRefinery Admin user@example.com")

def fetch_and_store_filings(symbol: str, db: Session):
    try:
        # Get company information by symbol to retrieve CIK
        company = edgar.Company(symbol)
        # Increased from .latest(10) to .latest(30) to capture 5+ years of filings
        # (5 annual 10-Ks + 20 quarterly 10-Qs)
        filings = company.get_filings(form=["10-K", "10-Q"]).latest(30)
        if not filings:
            return {"error": "No filings found for this symbol."}

        for filing in filings:
            filing_date = filing.filing_date
            period_of_report = filing.period_of_report

            # Convert period_of_report to date object if it's a string
            if isinstance(period_of_report, str):
                try:
                    period_of_report = datetime.strptime(period_of_report, "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    period_of_report = None
            elif not isinstance(period_of_report, date):
                period_of_report = None

            if filing.form == "10-K":
                # Extract year from period_of_report for 10-K
                year = period_of_report.year if period_of_report else None

                db_filing = Filing10K(
                    symbol=symbol,
                    filing_date=filing_date,
                    period_of_report=period_of_report,
                    year=year,
                    url=filing.url
                )
            elif filing.form == "10-Q":
                # Extract year and quarter from period_of_report for 10-Q
                year = period_of_report.year if period_of_report else None
                # Approximate quarter from month (Q1=Jan-Mar, Q2=Apr-Jun, Q3=Jul-Sep, Q4=Oct-Dec)
                quarter = ((period_of_report.month - 1) // 3) + 1 if period_of_report else None

                db_filing = Filing10Q(
                    symbol=symbol,
                    filing_date=filing_date,
                    period_of_report=period_of_report,
                    year=year,
                    quarter=quarter,
                    url=filing.url
                )
            else:
                continue

            db.add(db_filing)
        db.commit()
        return {"message": f"Filings for {symbol} have been stored."}
    except ValueError:
        return {"error": f"Symbol '{symbol}' not found in EDGAR database."}


def get_filings_by_symbol(symbol: str, db: Session):
    filings_10k = db.query(Filing10K).filter(Filing10K.symbol == symbol).all()
    filings_10q = db.query(Filing10Q).filter(Filing10Q.symbol == symbol).all()
    return filings_10k + filings_10q
