from src.domains.transactions.models import TransactionTable
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession


class TransactionRepository:

   async def insert_transaction(transaction_data, user_id, db: AsyncSession, rate):
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
    except Exception as e:
        await db.rollback()
        raise