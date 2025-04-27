import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv(
    "DB_URL",
    "postgresql+asyncpg://app:secret@localhost:5432/app",
)

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

async def get_session() -> AsyncSession:  # FastAPI‑style dependency
    async with async_session() as session:
        yield session

async def init_db() -> None:
    from models import models
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
