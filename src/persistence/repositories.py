from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Generic, TypeVar, Type, Optional, List
from src.persistence.models import Location, Billboard, Campaign, CampaignBillboard
from src.utils.uuid import generate_prefixed_uuid
from sqlmodel import select
from sqlalchemy.orm import selectinload
from datetime import date

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, id: str) -> Optional[T]:
        statement = select(self.model).where(self.model.id == id, self.model.is_deleted == False)
        result = await self.session.exec(statement)
        return result.first()

    async def get_all(self, offset: int = 0, limit: int = 100) -> List[T]:
        statement = select(self.model).where(self.model.is_deleted == False).offset(offset).limit(limit)
        result = await self.session.exec(statement)
        return result.all()

    async def update(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id: str) -> None:
        obj = await self.get(id)
        if obj:
            obj.is_deleted = True
            self.session.add(obj)
            await self.session.commit()

class LocationRepository(BaseRepository[Location]):
    async def create(self, obj: Location) -> Location:
        obj.id = generate_prefixed_uuid("loc")
        return await super().create(obj)
    
class BillboardRepository(BaseRepository[Billboard]):
    async def create(self, obj: Billboard) -> Billboard:
        obj.id = generate_prefixed_uuid("bill")
        return await super().create(obj)

    
    async def get_with_location(self, id: str) -> Billboard:
        statement = (
            select(self.model)
            .options(selectinload(self.model.location))
            .where(self.model.id == id, self.model.is_deleted == False)
        )
        result = await self.session.exec(statement)
        return result.first()
    
    async def get_all_with_location(self, offset: int = 0, limit: int = 100) -> List[Billboard]:
        statement = (
            select(self.model)
            .options(selectinload(self.model.location))
            .where(self.model.is_deleted == False)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.exec(statement)
        return result.all()
    
    async def get_all_by_location(self, id) -> List[Billboard]:
        statement = (
            select(self.model)
            .where(self.model.is_deleted == False, self.model.location_id == id)
        )
        result = await self.session.exec(statement)
        return result.all()

class CampaignRepository(BaseRepository[Campaign]):
    async def create(self, obj: Campaign) -> Campaign:
        obj.id = generate_prefixed_uuid("camp")
        return await super().create(obj)
    
class CampaignBillboardRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def link_billboard_campaign(self, campaign_id: str, billboard_id: str):
        link = CampaignBillboard(campaign_id=campaign_id, billboard_id=billboard_id)
        self.session.add(link)
        await self.session.commit()
        await self.session.refresh(link)
        return link

    async def unlink_billboard_campaign(self, campaign_id: str, billboard_id: str):
        statement = select(CampaignBillboard).where(
            CampaignBillboard.campaign_id == campaign_id,
            CampaignBillboard.billboard_id == billboard_id
        )
        result = await self.session.exec(statement)
        link = result.first()
        if link:
            await self.session.delete(link)
            await self.session.commit()
        return link

    async def get_billboards_for_campaign(self, campaign_id: str) -> List[Billboard]:
        statement = select(Billboard).options(selectinload(Billboard.location)).join(CampaignBillboard).where(CampaignBillboard.campaign_id == campaign_id)
        result = await self.session.exec(statement)
        return result.all()

    async def get_campaigns_for_billboard(self, billboard_id: str) -> List[Campaign]:
        statement = select(Campaign).join(CampaignBillboard).where(CampaignBillboard.billboard_id == billboard_id)
        result = await self.session.exec(statement)
        return result.all()

    async def get_available_billboards(self, start_date: date, end_date: date) -> List[Billboard]:
        # Billboards not linked to any campaign with overlapping dates
        subq = select(CampaignBillboard.billboard_id).join(Campaign).where(
            (Campaign.start_date <= end_date) & (Campaign.end_date >= start_date)
        )
        statement = select(Billboard).options(selectinload(Billboard.location)).where(~Billboard.id.in_(subq))
        result = await self.session.exec(statement)
        print('result', result)
        return result.all()