from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class TransactionCreate(BaseModel):
    source_currency: str = Field(..., pattern="^(BRL|USD|EUR|JPY)$")
    source_amount: float = Field(..., gt=0)
    target_currency: str = Field(..., pattern="^(BRL|USD|EUR|JPY)$")

class TransactionResponse(TransactionCreate):
    id: UUID
    user_id: UUID
    target_value: float
    conversion_rate: float
    timestamp: datetime

    class Config:
        from_attributes = True