from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas
import services.ticker_service as ticker_service
from typing import List

router = APIRouter()

@router.post("/tickers", response_model=schemas.Ticker)
async def add_ticker(ticker: schemas.Ticker, db: Session = Depends(get_db)):
    return ticker_service.create_ticker(db, ticker)

@router.get("/tickers", response_model=List[schemas.Ticker])
async def get_tickers(db: Session = Depends(get_db)):
    return ticker_service.get_all_tickers(db)

@router.get("/tickers/{symbol}/analyze")
async def analyze_ticker(symbol: str, db: Session = Depends(get_db)):
    return ticker_service.analyze_ticker_data(symbol, db)
