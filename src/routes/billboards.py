from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from supabase import Client

from src.dependencies import get_db, get_supabase
from src.domain.models.billboards import BillboardCreate, BillboardUpdate
from src.limiter import limiter
from src.services.billboards import BillboardService

router = APIRouter(prefix="/billboards", tags=["billboards"])

def wrap_data(result: Any) -> Dict[str, Any]:
    return {"data": result}

@router.post("/", response_model=Dict[str, Any], status_code=201)
@limiter.limit("100/minute")
async def create_billboard(request: Request, billboard: BillboardCreate, db: AsyncSession = Depends(get_db), supabase: Client = Depends(get_supabase)):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await BillboardService(db).create_billboard(billboard)
    return wrap_data(result)

@router.get("/{id}", response_model=Dict[str, Any])
@limiter.limit("100/minute")
async def billboard(request: Request, id: str, db: AsyncSession = Depends(get_db), supabase: Client = Depends(get_supabase)):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await BillboardService(db).get_billboard(id)
    return wrap_data(result)

@router.get("/", response_model=Dict[str, Any])
@limiter.limit("100/minute")
async def get_billboards(request: Request, offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), supabase: Client = Depends(get_supabase)):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await BillboardService(db).get_billboards(offset, limit)
    return wrap_data(result)

@router.delete("/{id}", status_code=204)
@limiter.limit("100/minute")
async def delete_billboard(request: Request, id: str, db: AsyncSession = Depends(get_db), supabase: Client = Depends(get_supabase)):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await BillboardService(db).delete_billboard(id)

@router.patch("/{id}", response_model=Dict[str, Any])
@limiter.limit("100/minute")
async def update_billboard(request: Request, id: str, billboard_update: BillboardUpdate, db: AsyncSession = Depends(get_db), supabase: Client = Depends(get_supabase)):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await BillboardService(db).update_billboard(id, billboard_update)
    return wrap_data(result)
