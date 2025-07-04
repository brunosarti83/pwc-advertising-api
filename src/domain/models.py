from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, Dict, Any

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