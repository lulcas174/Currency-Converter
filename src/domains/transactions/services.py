from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.infrastructure.services.exchange import ExchangeService
from .models import TransactionTable

class TransactionService:
    @staticmethod
    def create_transaction(
        db: Session,
        transaction_data,
        user_id: UUID
    ):
        if transaction_data.source_currency == transaction_data.target_currency:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Source and target currencies must be different"
            )

        try:
            rate = ExchangeService.calculate_rate(
                transaction_data.source_currency,
                transaction_data.target_currency
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Exchange service error: {str(e)}"
            )

        transaction = TransactionTable(
            user_id=user_id,
            source_currency=transaction_data.source_currency,
            source_amount=transaction_data.source_amount,
            target_currency=transaction_data.target_currency,
            conversion_rate=rate,
            target_value=transaction_data.source_amount * rate
        )

        try:
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

        return transaction

    @staticmethod
    def get_user_transactions(db: Session, user_id: UUID):
        return db.query(TransactionTable).filter(
            TransactionTable.user_id == user_id
        ).all()