from src.persistence.models import Billboard as BillboardDB, Location as LocationDB
from src.persistence.repositories import BillboardRepository, LocationRepository
from src.domain.models import Billboard, BillboardCreate, BillboardUpdate, HATEOASLinks, BillboardLocationInfo
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from typing import List

class BillboardService:
    def __init__(self, session: AsyncSession):
        self.repository = BillboardRepository(BillboardDB, session)
        self.location_repository = LocationRepository(LocationDB, session)

    async def create_billboard(self, billboard: BillboardCreate) -> Billboard:
        db_billboard = BillboardDB(**billboard.dict())
        created = await self.repository.create(db_billboard)
        location = await self.location_repository.get(created.location_id)
        location_info = BillboardLocationInfo(
            address=location.address,
            city=location.city,
            state=location.state,
            country_code=location.country_code,
            lat=location.lat,
            lng=location.lng
        ) if location else None
        links = HATEOASLinks(self=f"/api/v1/billboards/{created.id}")
        return Billboard(**created.dict(), links=links, location=location_info)

    async def get_billboard(self, id: str) -> Billboard:
        bill = await self.repository.get_with_location(id)
        if not bill:
            raise HTTPException(status_code=404, detail="Billboard not found")
        return Billboard(**bill.dict(), links=HATEOASLinks(self=f"/api/v1/billboards/{bill.id}"), location=BillboardLocationInfo(
            address=bill.location.address,
            city=bill.location.city,
            state=bill.location.state,
            country_code=bill.location.country_code,
            lat=bill.location.lat,
            lng=bill.location.lng
        ) if bill.location else None)

    async def get_billboards(self, offset: int = 0, limit: int = 100) -> List[Billboard]:
        billboards = await self.repository.get_all_with_location(offset, limit)
        return [Billboard(**bill.dict(), links=HATEOASLinks(self=f"/api/v1/billboards/{bill.id}"), location=BillboardLocationInfo(
            address=bill.location.address,
            city=bill.location.city,
            state=bill.location.state,
            country_code=bill.location.country_code,
            lat=bill.location.lat,
            lng=bill.location.lng
        ) if bill.location else None) for bill in billboards]

    async def update_billboard(self, id: str, billboard_update: BillboardUpdate) -> Billboard:
        billboard = await self.repository.get(id)
        if not billboard:
            raise HTTPException(status_code=404, detail="Billboard not found")
        update_data = billboard_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(billboard, key, value)
        await self.repository.update(billboard)
        location = await self.location_repository.get(billboard.location_id)
        location_info = BillboardLocationInfo(
            address=location.address,
            city=location.city,
            state=location.state,
            country_code=location.country_code,
            lat=location.lat,
            lng=location.lng
        ) if location else None
        links = HATEOASLinks(self=f"/api/v1/billboards/{id}")
        return Billboard(**billboard.dict(), links=links, location=location_info)

    async def delete_billboard(self, id: str) -> None:
        billboard = await self.repository.get(id)
        if not billboard:
            raise HTTPException(status_code=404, detail="Billboard not found")
        await self.repository.delete(id)