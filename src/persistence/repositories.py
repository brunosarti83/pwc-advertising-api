from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Generic, TypeVar, Type, Optional, List
from src.persistence.models import Location, Billboard, Campaign
from src.utils.uuid import generate_prefixed_uuid
from sqlmodel import select
from sqlalchemy.orm import selectinload

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