from asyncio import timeout
import datetime
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.domains.transactions.repositories import TransactionRepository
from src.domains.transactions.schemas import TransactionResponse
from src.infrastructure.services.exchange import ExchangeService
from .models import TransactionTable
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class TransactionService:
    @staticmethod
    async def create_transaction(db: AsyncSession, transaction_data, user_id: UUID):
        if transaction_data.source_currency == transaction_data.target_currency:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Source and target currencies must be different",
            )

        try:
            rate = await ExchangeService.calculate_rate(
                transaction_data.source_currency, 
                transaction_data.target_currency
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail=f"Exchange service error",
            )
        try:
            transaction_created = await TransactionRepository.insert_transaction(
                transaction_data=transaction_data,
                user_id=user_id,
                db=db,
                rate=rate,
            )
            transaction_data = transaction_created.__dict__       
            transaction_data["target_value"] = transaction_created.source_amount * transaction_created.conversion_rate
            transaction_data["id"] = transaction_created.id
            return TransactionResponse(**transaction_data)

        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Transaction creation failed: {str(e)}",
            )
        

    @staticmethod
    def get_user_transactions(db: Session, user_id: UUID):
        return (
            db.query(TransactionTable).filter(TransactionTable.user_id == user_id).all()
        )
