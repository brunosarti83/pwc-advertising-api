import os
from functools import lru_cache
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from supabase import Client, create_client

load_dotenv()

@lru_cache
def get_supabase() -> Client:
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@lru_cache
def get_db_engine() -> AsyncEngine:
    return create_async_engine(
        os.getenv("SUPABASE_DB_URL"),
        pool_size=5,
        max_overflow=10,
        connect_args={
            "statement_cache_size": 0,
            "server_settings": {
                "statement_timeout": "60s",  
                "idle_in_transaction_session_timeout": "30s" 
            }
        }
    )

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    engine = get_db_engine()
    async with AsyncSession(engine) as session:
        yield session
