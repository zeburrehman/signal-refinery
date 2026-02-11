from pydantic import BaseModel

class Ticker(BaseModel):
    symbol: str
    price: float
    market_cap: float

    class Config:
        orm_mode = True
