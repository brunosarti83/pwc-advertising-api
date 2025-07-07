from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List
from src.domain.models.billboards import Billboard
from src.domain.models.common import HATEOASLinks

class CampaignBase(BaseModel):
    name: str
    start_date: date
    end_date: date

class CampaignCreate(CampaignBase):
    pass

class Campaign(CampaignBase):
    id: str
    name: str
    start_date: date
    end_date: date
    created_at: datetime
    billboards: List[Billboard] = []
    total_dollar_amount: Optional[float] = 0
    links: HATEOASLinks

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None