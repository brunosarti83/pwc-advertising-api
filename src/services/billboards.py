import logging
from typing import List

from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.models.billboards import (
    Billboard,
    BillboardCreate,
    BillboardLocationInfo,
    BillboardUpdate,
)
from src.domain.models.common import HATEOASLinkObject, HATEOASLinks
from src.persistence.models import Billboard as BillboardDB
from src.persistence.models import Location as LocationDB
from src.persistence.repositories import BillboardRepository, LocationRepository


class BillboardService:
    def __init__(self, session: AsyncSession):
        self.repository = BillboardRepository(BillboardDB, session)
        self.location_repository = LocationRepository(LocationDB, session)

    async def create_billboard(self, billboard: BillboardCreate) -> Billboard:
        try:
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
            links = HATEOASLinks(
                self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/billboards/{created.id}"),
                actions=[
                    HATEOASLinkObject(name="update", method="PATCH", href=f"/api/v1/billboards/{created.id}"),
                    HATEOASLinkObject(name="delete", method="DELETE", href=f"/api/v1/billboards/{created.id}")
                ],
                related=[
                    HATEOASLinkObject(name="location", method="GET", href=f"/api/v1/locations/{created.location_id}")
                ]
            )
            return Billboard(**created.dict(), links=links, location=location_info)
        except HTTPException:
            raise
        except Exception as exc:
            logging.exception(f"Error creating billboard: {exc}")
            raise HTTPException(status_code=500, detail="Failed to create billboard")

    async def get_billboard(self, id: str) -> Billboard:
        try:
            bill = await self.repository.get_with_location(id)
            if not bill:
                raise HTTPException(status_code=404, detail="Billboard not found")
            return Billboard(
                **bill.dict(),
                location=BillboardLocationInfo(
                    address=bill.location.address,
                    city=bill.location.city,
                    state=bill.location.state,
                    country_code=bill.location.country_code,
                    lat=bill.location.lat,
                    lng=bill.location.lng
                ) if bill.location else None,
                links = HATEOASLinks(
                    self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/billboards/{bill.id}"),
                    actions=[
                        HATEOASLinkObject(name="update", method="PATCH", href=f"/api/v1/billboards/{bill.id}"),
                        HATEOASLinkObject(name="delete", method="DELETE", href=f"/api/v1/billboards/{bill.id}")
                    ],
                    related=[
                        HATEOASLinkObject(name="location", method="GET", href=f"/api/v1/locations/{bill.location_id}")
                    ]
                )
            )
        except HTTPException:
            raise
        except Exception as exc:
            logging.exception(f"Error getting billboard: {exc}")
            raise HTTPException(status_code=500, detail="Failed to get billboard")

    async def get_billboards(self, offset: int = 0, limit: int = 100) -> List[Billboard]:
        try:
            billboards = await self.repository.get_all_with_location(offset, limit)
            return [Billboard(
                **bill.dict(),
                location=BillboardLocationInfo(
                    address=bill.location.address,
                    city=bill.location.city,
                    state=bill.location.state,
                    country_code=bill.location.country_code,
                    lat=bill.location.lat,
                    lng=bill.location.lng
                ) if bill.location else None,
                links = HATEOASLinks(
                    self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/billboards/{bill.id}"),
                    actions=[
                        HATEOASLinkObject(name="update", method="PATCH", href=f"/api/v1/billboards/{bill.id}"),
                        HATEOASLinkObject(name="delete", method="DELETE", href=f"/api/v1/billboards/{bill.id}")
                    ],
                    related=[
                        HATEOASLinkObject(name="location", method="GET", href=f"/api/v1/locations/{bill.location_id}")
                    ]
                )
            ) for bill in billboards]
        except Exception as exc:
            logging.exception(f"Error getting billboards: {exc}")
            raise HTTPException(status_code=500, detail="Failed to get billboards")

    async def update_billboard(self, id: str, billboard_update: BillboardUpdate) -> Billboard:
        try:
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
            links = HATEOASLinks(self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/billboards/{id}"))
            return Billboard(**billboard.dict(), links=links, location=location_info)
        except HTTPException:
            raise
        except Exception as exc:
            logging.exception(f"Error updating billboard: {exc}")
            raise HTTPException(status_code=500, detail="Failed to update billboard")

    async def delete_billboard(self, id: str) -> None:
        try:
            billboard = await self.repository.get(id)
            if not billboard:
                raise HTTPException(status_code=404, detail="Billboard not found")
            await self.repository.delete(id)
        except HTTPException:
            raise
        except Exception as exc:
            logging.exception(f"Error deleting billboard: {exc}")
            raise HTTPException(status_code=500, detail="Failed to delete billboard")
