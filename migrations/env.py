from alembic import context
from sqlmodel import SQLModel
from src.dependencies import get_db_engine
from src.persistence.models import Location, Billboard, Campaign, CampaignBillboard

config = context.config
connectable = get_db_engine()
with connectable.connect() as connection:
    context.configure(connection=connection, target_metadata=SQLModel.metadata)
    with context.begin_transaction():
        context.run_migrations()