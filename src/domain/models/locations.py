from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.domain.models.common import HATEOASLinks


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
