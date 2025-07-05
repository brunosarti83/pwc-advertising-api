from sqlmodel import Session
from supabase import create_client, Client
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from functools import lru_cache
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

@lru_cache
def get_supabase() -> Client:
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@lru_cache
def get_db_engine() -> AsyncEngine:
    return create_async_engine(os.getenv("SUPABASE_DB_URL"))

def get_db() -> Generator[Session, None, None]:
    engine = get_db_engine()
    with Session(engine) as session:
        yield session