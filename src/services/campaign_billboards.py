from src.persistence.models import Billboard as BillboardDB, Campaign as CampaignDB
from src.persistence.repositories import CampaignBillboardRepository, CampaignRepository, BillboardRepository
from src.domain.models.billboards import Billboard, HATEOASLinks, BillboardLocationInfo
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from datetime import date
from fastapi import HTTPException

class CampaignBillboardService:
    def __init__(self, session: AsyncSession):
        self.repository = CampaignBillboardRepository(session)
        self.campaign_repository = CampaignRepository(CampaignDB, session)
        self.billboard_repository = BillboardRepository(BillboardDB, session)

    async def get_availability(self, start_date: date, end_date: date) -> List[Billboard]:
        available_billboards = await self.repository.get_available_billboards(start_date, end_date)
        if not available_billboards:
            return []
        return [
            Billboard(
                **b.dict(),
                location=BillboardLocationInfo(
                    address=b.location.address,
                    city=b.location.city,
                    state=b.location.state,
                    country_code=b.location.country_code,
                    lat=b.location.lat,
                    lng=b.location.lng
                ) if b.location else None,
                links=HATEOASLinks(self=f"/api/v1/billboards/{b.id}")
            )
            for b in available_billboards
        ]
    
    async def add_billboard_to_campaign(self, campaign_id: str, billboard_id: str) -> bool:
        campaign = await self.campaign_repository.get(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        billboard = await self.billboard_repository.get(billboard_id)
        if not billboard:
            raise HTTPException(status_code=404, detail="Billboard not found")
        available = await self.repository.check_billboard_availability(billboard_id, campaign.start_date, campaign.end_date)
        if not available:
            raise HTTPException(status_code=400, detail="Billboard is not available for this campaign")
        return await self.repository.link_billboard_campaign(campaign_id, billboard_id)