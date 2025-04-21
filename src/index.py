import asyncio

from contextlib import asynccontextmanager
from sqlite3 import OperationalError
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from src.config.settings import Settings
from src.infrastructure.database import engine, Base
from src.domains.users.routers import router as users_router
from src.routers import main_router
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.infrastructure.security import security_scheme
from sqlalchemy import text


settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("Database connection sucess!")
    except Exception as e:
        print("Erro to connect:", e)
    yield


app = FastAPI(
    title="API de conversão de moedas",
    lifespan=lifespan,
    swagger_ui_parameters={"docExpansion": "none"},
    # dependencies=[Depends(security_scheme)]
)


app.include_router(main_router)