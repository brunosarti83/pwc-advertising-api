from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from supabase import create_client, Client
from functools import lru_cache
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

load_dotenv()

@lru_cache
def get_supabase() -> Client:
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@lru_cache
def get_db_engine() -> AsyncEngine:
    return create_async_engine(os.getenv("SUPABASE_DB_URL"))

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    engine = get_db_engine()
    async with AsyncSession(engine) as session:
        yield session