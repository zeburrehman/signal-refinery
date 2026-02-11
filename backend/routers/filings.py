from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import services.filing_service as filing_service

router = APIRouter()

@router.post("/filings/{symbol}")
async def fetch_filings(symbol: str, db: Session = Depends(get_db)):
    result = filing_service.fetch_and_store_filings(symbol, db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/filings/{symbol}")
async def get_filings(symbol: str, db: Session = Depends(get_db)):
    return filing_service.get_filings_by_symbol(symbol, db)