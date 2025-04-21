from sqlalchemy import Column, Integer, String, Boolean, UUID, ForeignKey, Numeric, DateTime
from src.infrastructure.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class TransactionTable(Base):
    __tablename__ = "transactions"
    
    id = Column(UUID(), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    source_currency = Column(String(3), nullable=False, name="source_currency")
    source_amount = Column(Numeric, nullable=False, name="source_amount")
    target_currency = Column(String(3), nullable=False)
    conversion_rate = Column(Numeric, nullable=False, name="conversion_rate")
    timestamp = Column(DateTime(timezone=True), nullable=False)
    
    @property
    def target_value(self) -> Numeric:
        return self.source_amount * self.conversion_rate