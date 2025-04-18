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


settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            from src.infrastructure.database import recreate_tables
            await recreate_tables()
            break
        except OperationalError as e:
            if attempt == max_retries - 1:
                raise
            print(f"Database connection failed (attempt {attempt + 1}), retrying...")
            await asyncio.sleep(retry_delay)
    yield


app = FastAPI(
    title="API de conversão de moedas",
    lifespan=lifespan,
    swagger_ui_parameters={"docExpansion": "none"},
    # dependencies=[Depends(security_scheme)]
)


app.include_router(main_router)