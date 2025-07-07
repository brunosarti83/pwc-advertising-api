from src.persistence.models import Campaign as CampaignDB
from src.persistence.repositories import CampaignRepository
from src.persistence.repositories import CampaignBillboardRepository
from src.domain.models.campaigns import Campaign, CampaignCreate, CampaignUpdate
from src.domain.models.common import HATEOASLinks, HATEOASLinkObject
from src.domain.models.billboards import Billboard, BillboardLocationInfo
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from typing import List

class CampaignService:
    def __init__(self, session: AsyncSession):
        self.repository = CampaignRepository(CampaignDB, session)
        self.campaign_billboard_repository = CampaignBillboardRepository(session)

    async def create_campaign(self, campaign: CampaignCreate) -> Campaign:
        db_campaign = CampaignDB(**campaign.dict())
        created = await self.repository.create(db_campaign)
        links = HATEOASLinks(
            self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/campaigns/{created.id}"),
            actions=[
                HATEOASLinkObject(name="search_billboards", method="GET", href=f"/api/v1/availability/{created.id}"),
                HATEOASLinkObject(name="update", method="PATCH", href=f"/api/v1/campaigns/{created.id}"),
                HATEOASLinkObject(name="delete", method="DELETE", href=f"/api/v1/campaigns/{created.id}")
            ]
        )
        return Campaign(**created.dict(), links=links)

    async def get_campaign(self, id: str) -> Campaign:
        campaign = await self.repository.get(id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        billboards = await self.campaign_billboard_repository.get_billboards_for_campaign(id)
        billboard_objs = [
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
                links = HATEOASLinks(
                    self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/billboards/{b.id}"),
                    actions=[
                        HATEOASLinkObject(name="search_billboards", method="GET", href=f"/api/v1/availability/{b.id}"),
                        HATEOASLinkObject(name="remove_from_campaign", method="POST", href=f"/api/v1/campaigns/{id}/remove/{b.id}"),
                    ],
                    related=[
                        HATEOASLinkObject(name="location", method="GET", href=f"/api/v1/locations/{b.location.id}")
                    ]
                )
            ) for b in billboards
        ]
        days = (campaign.end_date - campaign.start_date).days + 1
        total_dollar_amount = sum(b.dollars_per_day * days for b in billboards)
        links = HATEOASLinks(
            self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/campaigns/{id}"),
            actions=[
                HATEOASLinkObject(name="search_billboards", method="GET", href=f"/api/v1/availability/{id}"),
                HATEOASLinkObject(name="update", method="PATCH", href=f"/api/v1/campaigns/{id}")
            ] + ([HATEOASLinkObject(name="delete", method="DELETE", href=f"/api/v1/campaigns/{id}")] if len(billboard_objs) == 0 else [])
        )
        return Campaign(
            **campaign.dict(),
            links=links,
            total_dollar_amount=total_dollar_amount,
            billboards=billboard_objs
        )

    async def get_campaigns(self, offset: int = 0, limit: int = 100) -> List[Campaign]:
        campaigns = await self.repository.get_all(offset, limit)
        result = []
        for camp in campaigns:
            billboards = await self.campaign_billboard_repository.get_billboards_for_campaign(camp.id)
            billboard_objs = [
                Billboard(
                    **b.dict(),
                    links=HATEOASLinks(self=f"/api/v1/billboards/{b.id}").dict(),
                    location=BillboardLocationInfo(
                        address=b.location.address,
                        city=b.location.city,
                        state=b.location.state,
                        country_code=b.location.country_code,
                        lat=b.location.lat,
                        lng=b.location.lng
                    ) if b.location else None
                ) for b in billboards
            ]
            days = (camp.end_date - camp.start_date).days + 1
            total_dollar_amount = sum(b.dollars_per_day * days for b in billboards)
            links = HATEOASLinks(
                self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/campaigns/{camp.id}"),
                actions=[
                    HATEOASLinkObject(name="search_billboards", method="GET", href=f"/api/v1/availability/{camp.id}"),
                    HATEOASLinkObject(name="update", method="PATCH", href=f"/api/v1/campaigns/{camp.id}")
                ] + ([HATEOASLinkObject(name="delete", method="DELETE", href=f"/api/v1/campaigns/{camp.id}")] if len(billboard_objs) == 0 else [])
            )
            result.append(Campaign(
                **camp.dict(),
                links=links,
                total_dollar_amount=total_dollar_amount,
                billboards=billboard_objs
            ))
        return result

    async def update_campaign(self, id: str, campaign_update: CampaignUpdate) -> Campaign:
        campaign = await self.repository.get(id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        update_data = campaign_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(campaign, key, value)
        await self.repository.update(campaign)
        links = HATEOASLinks(self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/campaigns/{id}"))
        return Campaign(**campaign.dict(), links=links)

    async def delete_campaign(self, id: str) -> None:
        campaign = await self.repository.get(id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")  
        await self.repository.delete(id)