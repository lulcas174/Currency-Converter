import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.transactions.repositories import TransactionRepository
from src.domains.transactions.schemas import TransactionResponse
from src.infrastructure.services.exchange import ExchangeService

logger = logging.getLogger(__name__)


class TransactionService:
    @staticmethod
    async def create_transaction(
            db: AsyncSession, transaction_data, user_id: UUID
    ) -> TransactionResponse:
        if transaction_data.source_currency == transaction_data.target_currency:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Source and target currencies must be different",
            )

        try:
            rate = await ExchangeService.calculate_rate(
                transaction_data.source_currency, transaction_data.target_currency
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Exchange service error",
            )
        try:
            transaction_created = await TransactionRepository.insert_transaction(
                transaction_data=transaction_data,
                user_id=user_id,
                db=db,
                rate=rate,
            )
            logger.info(f"Transaction created: {transaction_created.to_dict()}")
            return TransactionResponse(**transaction_created.to_dict())

        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Transaction creation failed: {str(e)}",
            )

    @staticmethod
    async def get_user_transactions(db: AsyncSession, user_id: UUID):
        try:
            return await TransactionRepository.get_user_transactions(
                db=db, user_id=user_id
            )
        except Exception as e:
            logger.critical(f"Unexpected error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno no servidor",
            )
