from fastapi import APIRouter, Depends, HTTPException, Request
from src.domain.models.billboards import Billboard, BillboardCreate, BillboardUpdate
from src.services.campaigns import CampaignService
from src.services.campaign_billboards import CampaignBillboardService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.dependencies import get_db, get_supabase
from supabase import Client
from typing import Any, Dict
from src.limiter import limiter

router = APIRouter(prefix="/availability", tags=["availability"])

def wrap_data(result: Any) -> Dict[str, Any]:
    return {"data": result}

@router.get("/", response_model=Dict[str, Any])
@limiter.limit("100/minute")
async def get_available_billboards(request: Request, campaign_id: str = "", start_date: str = "", end_date: str = "", db: AsyncSession = Depends(get_db), supabase: Client = Depends(get_supabase)):
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if campaign_id and (start_date or end_date):
        raise HTTPException(status_code=400, detail="Either provide a campaign_id or a start_date and end_date, but not both.")
    if campaign_id:
        campaign = await CampaignService(db).get_campaign(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        start_date = campaign.start_date
        end_date = campaign.end_date
    result = await CampaignBillboardService(db).get_availability(start_date, end_date)
    return wrap_data(result)