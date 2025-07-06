from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class HATEOASLinks(BaseModel):
    self: str
    related: Optional[Dict[str, str]] = None

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
    links: HATEOASLinks
    location: BillboardLocationInfo

class BillboardUpdate(BaseModel):
    location_id: Optional[str] = None
    width_mt: Optional[str] = None
    height_mt: Optional[str] = None
    dollars_per_day: Optional[str] = None