from fastapi import APIRouter, Depends, HTTPException, Request, Query
from src.domain.models.billboards import Billboard, BillboardCreate, BillboardUpdate
from src.services.campaigns import CampaignService
from src.services.campaign_billboards import CampaignBillboardService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.dependencies import get_db, get_supabase
from supabase import Client
from typing import Any, Dict
from src.limiter import limiter
from datetime import date

router = APIRouter(prefix="/availability", tags=["availability"])

def wrap_data(result: Any) -> Dict[str, Any]:
    return {"data": result}

@router.get("/", response_model=Dict[str, Any])
@limiter.limit("100/minute")
async def get_available_billboards(
    request: Request,
    campaign_id: str = "",
    start_date: date = None,
    end_date: date = None,
    db: AsyncSession = Depends(get_db),
    supabase: Client = Depends(get_supabase),
):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if isinstance(start_date, str):
        start_date = date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = date.fromisoformat(end_date)
    result = await CampaignBillboardService(db).get_availability(campaign_id, start_date, end_date)
    return wrap_data(result)