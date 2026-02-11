#!/usr/bin/env python3
"""Debug script to test filing_service in isolation"""

import sys
sys.path.insert(0, '.')

from database import SessionLocal
import services.filing_service as filing_service

if __name__ == "__main__":
    db = SessionLocal()
    print("Starting debug - about to call fetch_and_store_filings...")

    # Set breakpoint here - should hit line 11 in filing_service.py
    result = filing_service.fetch_and_store_filings("AAPL", db)
    print(f"Result: {result}")

    db.close()
