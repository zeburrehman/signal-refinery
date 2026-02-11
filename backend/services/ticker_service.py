from sqlalchemy.orm import Session
from database import TickerDB, FilingDB
import schemas
from datetime import datetime, timedelta

def create_ticker(db: Session, ticker: schemas.Ticker):
    db_ticker = TickerDB(**ticker.dict())
    db.add(db_ticker)
    db.commit()
    db.refresh(db_ticker)
    return db_ticker

def get_all_tickers(db: Session):
    return db.query(TickerDB).all()

def analyze_ticker_data(symbol: str, db: Session):
    ticker = db.query(TickerDB).filter(TickerDB.symbol == symbol).first()
    if not ticker:
        return {"message": "Ticker not found"}

    recent_filing = False
    last_filing_date = "N/A"
    ninety_days_ago = datetime.now() - timedelta(days=90)
    filings = db.query(FilingDB).filter(FilingDB.symbol == symbol).order_by(FilingDB.filing_date.desc()).all()
    
    if filings:
        last_filing_date = filings[0].filing_date
        filing_date = datetime.strptime(last_filing_date, "%Y-%m-%d")
        if filing_date > ninety_days_ago:
            recent_filing = True

    is_buy = ticker.price < 100 and ticker.market_cap > 1_000_000_000 and recent_filing
    
    return {
        "symbol": ticker.symbol,
        "signal": "Buy" if is_buy else "Hold",
        "reason": "Meets all criteria." if is_buy else "Does not meet all buy criteria.",
        "price": ticker.price,
        "market_cap": ticker.market_cap,
        "last_filing_date": last_filing_date
    }
