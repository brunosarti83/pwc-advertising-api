from sqlmodel import SQLModel, Field, Column, Date, TIMESTAMP, text
from datetime import datetime
from typing import Optional
from uuid import UUID

class Location(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)  # e.g., loc_<uuid>
    address: str
    city: str
    state: str
    country_code: str
    lat: float
    lng: float
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True)))
    is_deleted: bool = Field(default=False)

class Billboard(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)  # e.g., bill_<uuid>
    location_id: str = Field(foreign_key="locations.id")
    width_mt: float
    height_mt: float
    dollars_per_day: float
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True)))
    is_deleted: bool = Field(default=False)

class Campaign(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)  # e.g., cam_<uuid>
    name: str
    start_date: datetime = Field(sa_column=Column(Date))
    end_date: datetime = Field(sa_column=Column(Date))
    user_id: UUID = Field(foreign_key="auth.users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True)))
    is_deleted: bool = Field(default=False)

class CampaignBillboard(SQLModel, table=True):
    campaign_id: str = Field(foreign_key="campaigns.id", primary_key=True)
    billboard_id: str = Field(foreign_key="billboards.id", primary_key=True)