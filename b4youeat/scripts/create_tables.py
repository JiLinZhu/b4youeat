"""
Create all SQLAlchemy tables inside the running database.

Usage (from repo root):
    docker compose run --rm server python -m scripts.create_tables
"""
import asyncio
from db import engine
from models.models import Base


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅  All tables created.")


if __name__ == "__main__":
    asyncio.run(main())