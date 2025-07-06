from src.persistence.models import Campaign as CampaignDB
from src.persistence.models import Billboard as BillboardDB
from src.persistence.repositories import CampaignRepository
from src.domain.models.campaigns import Campaign, CampaignCreate, CampaignUpdate, HATEOASLinks
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from typing import List

class CampaignService:
    def __init__(self, session: AsyncSession):
        self.repository = CampaignRepository(CampaignDB, session)

    async def create_campaign(self, campaign: CampaignCreate) -> Campaign:
        db_campaign = CampaignDB(**campaign.dict())
        created = await self.repository.create(db_campaign)
        links = HATEOASLinks(self=f"/api/v1/campaigns/{created.id}")
        return Campaign(**created.dict(), links=links)

    async def get_campaign(self, id: str) -> Campaign:
        campaign = await self.repository.get(id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        links = HATEOASLinks(self=f"/api/v1/campaigns/{id}")
        return Campaign(**campaign.dict(), links=links)

    async def get_campaigns(self, offset: int = 0, limit: int = 100) -> List[Campaign]:
        campaigns = await self.repository.get_all(offset, limit)
        return [Campaign(**camp.dict(), links=HATEOASLinks(self=f"/api/v1/campaigns/{camp.id}")) for camp in campaigns]

    async def update_campaign(self, id: str, campaign_update: CampaignUpdate) -> Campaign:
        campaign = await self.repository.get(id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        update_data = campaign_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(campaign, key, value)
        await self.repository.update(campaign)
        links = HATEOASLinks(self=f"/api/v1/campaigns/{id}")
        return Campaign(**campaign.dict(), links=links)

    async def delete_campaign(self, id: str) -> None:
        campaign = await self.repository.get(id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")  
        await self.repository.delete(id)