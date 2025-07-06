from src.persistence.repositories import CampaignBillboardRepository
from src.domain.models.billboards import Billboard, HATEOASLinks, BillboardLocationInfo
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from datetime import date

class CampaignBillboardService:
    def __init__(self, session: AsyncSession):
        self.repository = CampaignBillboardRepository(session)

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