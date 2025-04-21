from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.infrastructure.security import TokenData, get_current_user
from .schemas import TransactionCreate, TransactionResponse
from .services import TransactionService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/transactions", 
    tags=["transactions"],
    dependencies=[Security(get_current_user, scopes=[])]
)

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    try:
        return await TransactionService.create_transaction(
            db=db,
            transaction_data=transaction,
            user_id=current_user.user_id
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/user", response_model=list[TransactionResponse])
async def get_user_transactions(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    transactions = TransactionService.get_user_transactions(
        db=db,
        user_id=current_user.user_id
    )
    if not transactions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No transactions found"
        )
    return transactions