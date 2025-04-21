import uuid

from sqlalchemy import Column, String, ForeignKey, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.database import Base


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

    def to_dict(self):
        return {
            "transaction_id": self.id,
            "user_id": self.user_id,
            "source_currency": self.source_currency,
            "source_amount": self.source_amount,
            "target_currency": self.target_currency,
            "conversion_rate": self.conversion_rate,
            "timestamp": self.timestamp,
            "target_value": self.source_amount * self.conversion_rate,
        }
