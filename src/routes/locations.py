from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from supabase import Client

from src.dependencies import get_db, get_supabase
from src.domain.models.locations import LocationCreate, LocationUpdate
from src.limiter import limiter
from src.services.locations import LocationService

router = APIRouter(prefix="/locations", tags=["locations"])

def wrap_data(result: Any, **kwargs) -> Dict[str, Any]:
    return {"data": result, **kwargs}

@router.post("/", response_model=Dict[str, Any], status_code=201)
@limiter.limit("100/minute")
async def create_location(request: Request, location: LocationCreate, db: AsyncSession = Depends(get_db), supabase: Client = Depends(get_supabase)):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await LocationService(db).create_location(location)
    return wrap_data(result)

@router.get("/{id}", response_model=Dict[str, Any])
@limiter.limit("100/minute")
async def get_location(request: Request, id: str, db: AsyncSession = Depends(get_db), supabase: Client = Depends(get_supabase)):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await LocationService(db).get_location(id)
    return wrap_data(result)

@router.get("/", response_model=Dict[str, Any])
@limiter.limit("100/minute")
async def get_locations(request: Request, offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), supabase: Client = Depends(get_supabase)):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await LocationService(db).get_locations(offset, limit)
    return wrap_data(result)

@router.delete("/{id}", status_code=204)
@limiter.limit("100/minute")
async def delete_location(request: Request, id: str, db: AsyncSession = Depends(get_db), supabase: Client = Depends(get_supabase)):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await LocationService(db).delete_location(id)

@router.patch("/{id}", response_model=Dict[str, Any])
@limiter.limit("100/minute")
async def update_location(request: Request, id: str, location_update: LocationUpdate, db: AsyncSession = Depends(get_db), supabase: Client = Depends(get_supabase)):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await LocationService(db).update_location(id, location_update)
    return wrap_data(result)
