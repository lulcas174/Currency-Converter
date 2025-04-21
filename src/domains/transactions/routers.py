import logging

from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database import get_db
from src.infrastructure.security import TokenData, get_current_user
from .schemas import (TransactionCreate,
                      TransactionListResponse,
                      TransactionResponse)
from .services import TransactionService

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    dependencies=[Security(get_current_user, scopes=[])],
)
logger = logging.getLogger(__name__)


@router.post(
    "/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED
)
async def create_transaction(
        transaction: TransactionCreate,
        db: AsyncSession = Depends(get_db),
        current_user: TokenData = Depends(get_current_user),
) -> TransactionResponse:
    try:
        created_transaction = await TransactionService.create_transaction(
            db=db, transaction_data=transaction, user_id=current_user.user_id
        )

        return created_transaction

    except HTTPException as http_error:
        raise http_error

    except Exception as unexpected_error:
        logger.error(f"Error in process transaction: {str(unexpected_error)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the transaction",
        )


@router.get("/list")
async def get_user_transactions(
        db: AsyncSession = Depends(get_db),
        current_user: TokenData = Depends(get_current_user),
):
    transactions = await TransactionService.get_user_transactions(
        db=db, user_id=current_user.user_id
    )

    if not transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No transactions found"
        )

    return TransactionListResponse(
        transactions=[transaction.to_dict() for transaction in transactions]
    )
