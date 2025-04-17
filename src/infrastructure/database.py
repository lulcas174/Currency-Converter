from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config.settings import settings

import importlib
import pathlib

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

def load_all_models():
    """
    Importa todos os arquivos 'models.py' dentro dos subdiretórios de 'src/domains'
    para garantir que todas as tabelas estejam registradas no Base.metadata.
    """
    base_path = pathlib.Path(__file__).resolve().parent.parent / "domains"
    module_base = "src.domains"

    for module in base_path.iterdir():
        if module.is_dir() and (module / "models.py").exists():
            importlib.import_module(f"{module_base}.{module.name}.models")

# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

async def recreate_tables():
    load_all_models()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
