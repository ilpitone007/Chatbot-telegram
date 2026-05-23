from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import config
import os

# Assicurati che la directory esista per SQLite
db_path = config.database_url.replace("sqlite+aiosqlite:///", "")
if db_path.startswith("./"):
    os.makedirs(os.path.dirname(db_path[2:]), exist_ok=True)
elif not db_path.startswith("sqlite") and not db_path.startswith("memory"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

engine = create_async_engine(
    config.database_url,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
