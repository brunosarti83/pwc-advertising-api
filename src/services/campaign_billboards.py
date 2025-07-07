import logging
from datetime import date
from typing import List

from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.models.billboards import Billboard, BillboardLocationInfo, HATEOASLinks
from src.domain.models.common import HATEOASLinkObject
from src.persistence.models import Billboard as BillboardDB
from src.persistence.models import Campaign as CampaignDB
from src.persistence.repositories import (
    BillboardRepository,
    CampaignBillboardRepository,
    CampaignRepository,
)


class CampaignBillboardService:
    def __init__(self, session: AsyncSession):
        self.repository = CampaignBillboardRepository(session)
        self.campaign_repository = CampaignRepository(CampaignDB, session)
        self.billboard_repository = BillboardRepository(BillboardDB, session)

    async def get_availability(self, campaign_id: str, start_date: date, end_date: date) -> List[Billboard]:
        try:
            if campaign_id and (start_date or end_date):
                raise HTTPException(status_code=400, detail="Either provide a campaign_id or a start_date and end_date, but not both.")
            if campaign_id:
                campaign = await self.campaign_repository.get(campaign_id)
                if not campaign:
                    raise HTTPException(status_code=404, detail="Campaign not found")
                start_date = campaign.start_date
                end_date = campaign.end_date
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
                    links=HATEOASLinks(
                        self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/billboards/{b.id}"),
                        actions=([
                            HATEOASLinkObject(name="add_to_campaign", method="POST", href=f"/api/v1/campaigns/{campaign_id}/add/{b.id}")
                        ] if campaign_id else None)
                    )
                )
                for b in available_billboards
            ]
        except HTTPException:
            raise
        except Exception as exc:
            logging.exception(f"Error getting availability: {exc}")
            raise HTTPException(status_code=500, detail="Failed to get billboard availability")

    async def add_billboard_to_campaign(self, campaign_id: str, billboard_id: str) -> dict:
        try:
            campaign = await self.campaign_repository.get(campaign_id)
            if not campaign:
                raise HTTPException(status_code=404, detail="Campaign not found")
            billboard = await self.billboard_repository.get(billboard_id)
            if not billboard:
                raise HTTPException(status_code=404, detail="Billboard not found")
            available = await self.repository.check_billboard_availability(billboard_id, campaign.start_date, campaign.end_date)
            if not available:
                raise HTTPException(status_code=400, detail="Billboard is not available for this campaign")
            await self.repository.link_billboard_campaign(campaign_id, billboard_id)
            links = HATEOASLinks(
                actions=[
                    HATEOASLinkObject(name="undo", method="POST", href=f"/api/v1/campaigns/{campaign_id}/remove/{billboard_id}")
                ],
                related=[
                    HATEOASLinkObject(name="billboard", method="GET", href=f"/api/v1/billboards/{billboard_id}"),
                    HATEOASLinkObject(name="campaign", method="GET", href=f"/api/v1/campaigns/{campaign_id}")
                ]
            )
            return {"message": "Billboard added to campaign", "links": links}
        except HTTPException:
            raise
        except Exception as exc:
            logging.exception(f"Error adding billboard to campaign: {exc}")
            raise HTTPException(status_code=500, detail="Failed to add billboard to campaign")

    async def remove_billboard_from_campaign(self, campaign_id: str, billboard_id: str) -> dict:
        try:
            campaign = await self.campaign_repository.get(campaign_id)
            if not campaign:
                raise HTTPException(status_code=404, detail="Campaign not found")
            billboard = await self.billboard_repository.get(billboard_id)
            if not billboard:
                raise HTTPException(status_code=404, detail="Billboard not found")
            await self.repository.unlink_billboard_campaign(campaign_id, billboard_id)
            links = HATEOASLinks(
                actions=[
                    HATEOASLinkObject(name="undo", method="POST", href=f"/api/v1/campaigns/{campaign_id}/add/{billboard_id}")
                ],
                related=[
                    HATEOASLinkObject(name="billboard", method="GET", href=f"/api/v1/billboards/{billboard_id}"),
                    HATEOASLinkObject(name="campaign", method="GET", href=f"/api/v1/campaigns/{campaign_id}")
                ]
            )
            return {"message": "Billboard removed from campaign", "links": links}
        except HTTPException:
            raise
        except Exception as exc:
            logging.exception(f"Error removing billboard from campaign: {exc}")
            raise HTTPException(status_code=500, detail="Failed to remove billboard from campaign")
