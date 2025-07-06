from fastapi import APIRouter, Depends, HTTPException, Request
from src.domain.models.campaigns import Campaign, CampaignCreate, CampaignUpdate
from src.services.campaigns import CampaignService
from src.services.campaign_billboards import CampaignBillboardService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.dependencies import get_db, get_supabase
from supabase import Client
from typing import Any, Dict
from src.limiter import limiter

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

def wrap_data(result: Any, **kwargs) -> Dict[str, Any]:
    return {"data": result, **kwargs}

@router.post("/", response_model=Dict[str, Any], status_code=201)
@limiter.limit("100/minute")
async def create_campaign(
    request: Request, 
    campaign: CampaignCreate, 
    db: AsyncSession = Depends(get_db), 
    supabase: Client = Depends(get_supabase)
):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await CampaignService(db).create_campaign(campaign)
    return wrap_data(result)

@router.get("/{id}", response_model=Dict[str, Any])
@limiter.limit("100/minute")
async def get_campaign(
    request: Request, 
    id: str, 
    db: AsyncSession = Depends(get_db), 
    supabase: Client = Depends(get_supabase)
):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await CampaignService(db).get_campaign(id)
    return wrap_data(result)

@router.get("/", response_model=Dict[str, Any])
@limiter.limit("100/minute")
async def get_campaigns(
    request: Request, 
    offset: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db), 
    supabase: Client = Depends(get_supabase)
):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await CampaignService(db).get_campaigns(offset, limit)
    return wrap_data(result)

@router.delete("/{id}", status_code=204)
@limiter.limit("100/minute")
async def delete_campaign(
    request: Request, 
    id: str, 
    db: AsyncSession = Depends(get_db), 
    supabase: Client = Depends(get_supabase)
):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await CampaignService(db).delete_campaign(id)

@router.patch("/{id}", response_model=Dict[str, Any])
@limiter.limit("100/minute")
async def update_campaign(
    request: Request, 
    id: str, 
    campaign_update: CampaignUpdate, 
    db: AsyncSession = Depends(get_db), 
    supabase: Client = Depends(get_supabase)
):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await CampaignService(db).update_campaign(id, campaign_update)
    return wrap_data(result)

@router.post("/{id}/add/{billboard_id}", response_model=Dict[str, Any])
@limiter.limit("100/minute")
async def add_billboard_to_campaign(
    request: Request, 
    id: str, 
    billboard_id: str, 
    db: AsyncSession = Depends(get_db), 
    supabase: Client = Depends(get_supabase)
):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await CampaignBillboardService(db).add_billboard_to_campaign(id, billboard_id)
    return { "message": "Billboard added to campaign", **wrap_data(result) } # undo, add_more

@router.post("/{id}/remove/{billboard_id}", response_model=Dict[str, Any])
@limiter.limit("100/minute")
async def remove_billboard_from_campaign(
    request: Request, 
    id: str, 
    billboard_id: str, 
    db: AsyncSession = Depends(get_db), 
    supabase: Client = Depends(get_supabase)
):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = await CampaignBillboardService(db).remove_billboard_from_campaign(id, billboard_id)
    return { "message": "Billboard removed from campaign", **wrap_data(result) } # undo back_to_campaign add_another