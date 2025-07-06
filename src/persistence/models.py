from sqlmodel import SQLModel, Field, Column, Date, TIMESTAMP, text
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID
from sqlmodel import Relationship

if TYPE_CHECKING:
    from .models import Billboard, Location

class Location(SQLModel, table=True):
    __tablename__ = "locations"
    id: str = Field(default=None, primary_key=True)  # loc_<uuid>
    address: str
    city: str
    state: str
    country_code: str
    lat: float
    lng: float
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True)))
    is_deleted: bool = Field(default=False)
    billboards: List["Billboard"] = Relationship(back_populates="location")

class Billboard(SQLModel, table=True):
    __tablename__ = "billboards"
    id: str = Field(default=None, primary_key=True)  # bill_<uuid>
    location_id: str = Field(foreign_key="locations.id")
    width_mt: float
    height_mt: float
    dollars_per_day: float
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True)))
    is_deleted: bool = Field(default=False)
    location: Optional["Location"] = Relationship(back_populates="billboards")

class Campaign(SQLModel, table=True):
    __tablename__ = "campaigns"
    id: str = Field(default=None, primary_key=True)  # cam_<uuid>
    name: str
    start_date: datetime = Field(sa_column=Column(Date))
    end_date: datetime = Field(sa_column=Column(Date))
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True)))
    is_deleted: bool = Field(default=False)

class CampaignBillboard(SQLModel, table=True):
    __tablename__ = "campaign_billboards"
    campaign_id: str = Field(foreign_key="campaigns.id", primary_key=True)
    billboard_id: str = Field(foreign_key="billboards.id", primary_key=True)