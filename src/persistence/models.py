from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import TIMESTAMP, Column, Date, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .models import Billboard, Campaign, CampaignBillboard, Location

class CampaignBillboard(SQLModel, table=True):
    __tablename__ = "campaign_billboards"
    campaign_id: str = Field(foreign_key="campaigns.id", primary_key=True)
    billboard_id: str = Field(foreign_key="billboards.id", primary_key=True)
    campaign: "Campaign" = Relationship(back_populates="billboard_links")
    billboard: "Billboard" = Relationship(back_populates="campaign_links")

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
    campaign_links: List["CampaignBillboard"] = Relationship(back_populates="billboard")
    campaigns: List["Campaign"] = Relationship(
        back_populates="billboards",
        link_model=CampaignBillboard
    )

class Campaign(SQLModel, table=True):
    __tablename__ = "campaigns"
    id: str = Field(default=None, primary_key=True)  # cam_<uuid>
    name: str
    start_date: date = Field(sa_column=Column(Date))
    end_date: date = Field(sa_column=Column(Date))
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True)))
    is_deleted: bool = Field(default=False)
    billboard_links: List["CampaignBillboard"] = Relationship(back_populates="campaign")
    billboards: List["Billboard"] = Relationship(
        back_populates="campaigns",
        link_model=CampaignBillboard
    )
