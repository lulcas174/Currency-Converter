from fastapi import APIRouter
from src.domains.users.routers import router as users_router
from src.domains.transactions.routers import router as transactions_router

main_router = APIRouter()

main_router.include_router(users_router, prefix="/api/v1")
main_router.include_router(transactions_router, prefix="/api/v1")