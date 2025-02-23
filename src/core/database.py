from contextlib import asynccontextmanager
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

# Get database connection parameters from environment variables
db_user = os.getenv("PINGDOM_STORE_USER", "postgres")
db_password = os.getenv("PINGDOM_STORE_PASSWORD", "postgres")
db_host = os.getenv("PINGDOM_STORE_HOST", "postgresql")
db_port = os.getenv("PINGDOM_STORE_PORT", "5432")
db_name = os.getenv("PINGDOM_STORE_DBNAME", "pingdom")

# Construct the async database URL
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create the async engine
engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> AsyncSession:
    """Get a database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db():
    """Initialize the database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
