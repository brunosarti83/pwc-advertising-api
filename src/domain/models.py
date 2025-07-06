from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, Dict, Any

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class SupabaseSession(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None
    user: Optional[Any] = None

class HATEOASLinks(BaseModel):
    self: str
    related: Optional[Dict[str, str]] = None

class LocationBase(BaseModel):
    address: str
    city: str
    state: str
    country_code: str
    lat: float
    lng: float

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: str
    created_at: datetime
    links: HATEOASLinks

class LocationUpdate(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country_code: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

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