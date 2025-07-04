from fastapi import APIRouter, Depends, HTTPException
from src.domain.models import Location, LocationCreate, LocationUpdate
from src.services.locations import LocationService
from sqlmodel import Session
from src.dependencies import get_db, get_supabase
from supabase import Client
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/locations", tags=["locations"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/", response_model=Location, status_code=201)
@limiter.limit("100/minute")
async def create_location(location: LocationCreate, db: Session = Depends(get_db), supabase: Client = Depends(get_supabase)):
    # Supabase Auth: Verify JWT (example, to be expanded)
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return LocationService(db).create_location(location)

@router.get("/{id}", response_model=Location)
@limiter.limit("100/minute")
async def get_location(id: str, db: Session = Depends(get_db), supabase: Client = Depends(get_supabase)):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return LocationService(db).get_location(id)

@router.get("/", response_model=List[Location])
@limiter.limit("100/minute")
async def get_locations(offset: int = 0, limit: int = 100, db: Session = Depends(get_db), supabase: Client = Depends(get_supabase)):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return LocationService(db).get_locations(offset, limit)

@router.delete("/{id}", status_code=204)
@limiter.limit("100/minute")
async def delete_location(id: str, db: Session = Depends(get_db), supabase: Client = Depends(get_supabase)):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    LocationService(db).delete_location(id)