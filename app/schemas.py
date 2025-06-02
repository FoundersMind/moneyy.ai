from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Trade(BaseModel):
    ticker: str
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)
    side: str  # "buy" or "sell"
    timestamp: Optional[datetime] = None

class TradeQuery(BaseModel):
    ticker: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
