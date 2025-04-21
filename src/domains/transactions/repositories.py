from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.transactions.models import TransactionTable


class TransactionRepository:

    @staticmethod
    async def insert_transaction(
        transaction_data,
        user_id,
        db: AsyncSession,
        rate
    ):
        try:
            transaction = TransactionTable(
                user_id=user_id,
                source_currency=transaction_data.source_currency,
                source_amount=transaction_data.source_amount,
                target_currency=transaction_data.target_currency,
                conversion_rate=rate,
                timestamp=datetime.now(timezone.utc),
            )
            db.add(transaction)
            await db.commit()
            await db.refresh(transaction)
            return transaction
        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def get_user_transactions(db: AsyncSession, user_id):
        try:
            result = await db.execute(
                select(TransactionTable)
                .where(TransactionTable.user_id == user_id)
            )
            return result.scalars().all()
        except Exception:
            await db.rollback()
            raise
