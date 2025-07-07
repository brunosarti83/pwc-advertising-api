from src.persistence.models import Location as LocationDB
from src.persistence.models import Billboard as BillboardDB
from src.persistence.repositories import LocationRepository, BillboardRepository
from src.domain.models.locations import Location, LocationCreate, LocationUpdate
from src.domain.models.common import HATEOASLinks, HATEOASLinkObject
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from typing import List

class LocationService:
    def __init__(self, session: AsyncSession):
        self.repository = LocationRepository(LocationDB, session)
        self.billboards_repository = BillboardRepository(BillboardDB, session)

    async def create_location(self, location: LocationCreate) -> Location:
        db_location = LocationDB(**location.dict())
        created = await self.repository.create(db_location)
        links = HATEOASLinks(
            self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/locations/{created.id}"),
            actions=[
                HATEOASLinkObject(name="update", method="PATCH", href=f"/api/v1/locations/{created.id}"),
                HATEOASLinkObject(name="delete", method="DELETE", href=f"/api/v1/locations/{created.id}")
            ]
        )
        return Location(**created.dict(), links=links)

    async def get_location(self, id: str) -> Location:
        location = await self.repository.get(id)
        billboards_at_location = await self.billboards_repository.get_all_by_location(id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        links = HATEOASLinks(
            self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/locations/{location.id}"),
            actions=[
                HATEOASLinkObject(name="update", method="PATCH", href=f"/api/v1/locations/{location.id}"), 
            ] + ([HATEOASLinkObject(name="delete", method="DELETE", href=f"/api/v1/locations/{location.id}")] if len(billboards_at_location) == 0 else []),
            related=[
                HATEOASLinkObject(name="billboard", method="GET", href=f"/api/v1/billboards/{bill.id}") for bill in billboards_at_location
            ]
        ) 
        return Location(**location.dict(), links=links)

    async def get_locations(self, offset: int = 0, limit: int = 100) -> List[Location]:
        locations = await self.repository.get_all(offset, limit)
        return [Location(
            **loc.dict(), 
            links = HATEOASLinks(self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/locations/{loc.id}"))
        ) for loc in locations]

    async def update_location(self, id: str, location_update: LocationUpdate) -> Location:
        location = await self.repository.get(id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        update_data = location_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(location, key, value)
        await self.repository.update(location)
        links = HATEOASLinks(self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/locations/{id}"))
        return Location(**location.dict(), links=links)

    async def delete_location(self, id: str) -> None:
        location = await self.repository.get(id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        billboards = await self.billboards_repository.get_all_by_location(id)
        if len(billboards) > 0:
            raise HTTPException(status_code=409, detail="Location has billboards, update billboards first")   
        await self.repository.delete(id)