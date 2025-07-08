from logging.config import fileConfig

from alembic import context
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine

from src.dependencies import get_db_engine
from src.persistence.models import Billboard, Campaign, CampaignBillboard, Location

config = context.config
fileConfig(config.config_file_name)
connectable = get_db_engine()

# Get reed of possible old metadata
# SQLModel.metadata.clear()
# SQLModel.metadata.create_all(bind=connectable, tables=[
#     Location.__table__,
#     Billboard.__table__,
#     Campaign.__table__,
#     CampaignBillboard.__table__
# ])

# Configure Alembic to handle SQLModel types - imports sqlmodel if sqlmodel types are used
def render_item(type_, obj, autogen_context):
    """Customize rendering of SQLModel types in migration scripts."""
    if type_ == "type" and hasattr(obj, "__module__") and obj.__module__.startswith("sqlmodel"):
        autogen_context.imports.add("import sqlmodel")
        return f"sqlmodel.sql.sqltypes.{obj.__class__.__name__}()"
    return False

import asyncio

async def run_async_migrations():
    async with connectable.begin() as connection:
        await connection.run_sync(
            lambda conn: context.configure(
                connection=conn,
                target_metadata=SQLModel.metadata
            )
        )
        await connection.run_sync(lambda conn: context.run_migrations())

asyncio.run(run_async_migrations())
