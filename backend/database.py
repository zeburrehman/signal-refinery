from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, UniqueConstraint, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Use PostgreSQL in Docker, fallback to SQLite for local development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./tickers.db"
)

# Ensure the database URL is in the correct format for SQLAlchemy
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600,   # Recycle connections after 1 hour
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Filing10K(Base):
    __tablename__ = "filings_10k"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    filing_date = Column(Date, index=True)
    period_of_report = Column(Date, index=True)
    accepted_date = Column(DateTime)
    url = Column(String)
    year = Column(Integer, index=True)

    __table_args__ = (
        UniqueConstraint('symbol', 'filing_date', 'url', name='_10k_unique'),
    )

class Filing10Q(Base):
    __tablename__ = "filings_10q"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    filing_date = Column(Date, index=True)
    period_of_report = Column(Date, index=True)
    accepted_date = Column(DateTime)
    url = Column(String)
    year = Column(Integer, index=True)
    quarter = Column(Integer, index=True)

    __table_args__ = (
        UniqueConstraint('symbol', 'filing_date', 'url', name='_10q_unique'),
    )

class FinancialData(Base):
    __tablename__ = "financial_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    filing_type = Column(String, index=True)
    filing_date = Column(Date, index=True)
    period_start = Column(Date, index=True, nullable=True)
    period_end = Column(Date, index=True)

    statement_type = Column(String, index=True)
    metric_name = Column(String, index=True)
    metric_label = Column(String)
    value = Column(Float)
    unit = Column(String)

    extracted_date = Column(DateTime, default=datetime.now)

    __table_args__ = (
        UniqueConstraint('symbol', 'filing_date', 'statement_type', 'metric_name', 'period_end', name='_financial_data_unique'),
    )

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
