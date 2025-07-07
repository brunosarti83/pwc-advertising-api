from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict
from src.domain.models.common import HATEOASLinks

class BillboardBase(BaseModel):
    location_id: str
    width_mt: float
    height_mt: float
    dollars_per_day: float

class BillboardLocationInfo(BaseModel):
    address: str
    city: str
    state: str
    country_code: str
    lat: float
    lng: float

class BillboardCreate(BillboardBase):
    pass

class Billboard(BillboardBase):
    id: str
    created_at: datetime
    location: BillboardLocationInfo
    links: HATEOASLinks

class BillboardUpdate(BaseModel):
    location_id: Optional[str] = None
    width_mt: Optional[str] = None
    height_mt: Optional[str] = None
    dollars_per_day: Optional[str] = None