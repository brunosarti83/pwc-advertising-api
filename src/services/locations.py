import csv
import logging
from typing import List, IO, Dict, Any

from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.models.common import HATEOASLinkObject, HATEOASLinks
from src.domain.models.locations import Location, LocationCreate, LocationUpdate
from src.persistence.models import Billboard as BillboardDB
from src.persistence.models import Location as LocationDB
from src.persistence.repositories import BillboardRepository, LocationRepository
from src.utils.uuid import generate_prefixed_uuid


class LocationService:
    def __init__(self, session: AsyncSession):
        self.repository = LocationRepository(LocationDB, session)
        self.billboards_repository = BillboardRepository(BillboardDB, session)

    async def create_location(self, location: LocationCreate) -> Location:
        try:
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
        except HTTPException:
            raise
        except Exception as exc:
            logging.exception(f"Error creating location: {exc}")
            raise HTTPException(status_code=500, detail="Failed to create location")

    async def get_location(self, id: str) -> Location:
        try:
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
        except HTTPException:
            raise
        except Exception as exc:
            logging.exception(f"Error getting location: {exc}")
            raise HTTPException(status_code=500, detail="Failed to get location")

    async def get_locations(self, offset: int = 0, limit: int = 100) -> List[Location]:
        try:
            locations = await self.repository.get_all(offset, limit)
            return [Location(
                **loc.dict(),
                links = HATEOASLinks(self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/locations/{loc.id}"))
            ) for loc in locations]
        except Exception as exc:
            logging.exception(f"Error getting locations: {exc}")
            raise HTTPException(status_code=500, detail="Failed to get locations")

    async def update_location(self, id: str, location_update: LocationUpdate) -> Location:
        try:
            location = await self.repository.get(id)
            if not location:
                raise HTTPException(status_code=404, detail="Location not found")
            update_data = location_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(location, key, value)
            await self.repository.update(location)
            links = HATEOASLinks(self=HATEOASLinkObject(name="self", method="GET", href=f"/api/v1/locations/{id}"))
            return Location(**location.dict(), links=links)
        except HTTPException:
            raise
        except Exception as exc:
            logging.exception(f"Error updating location: {exc}")
            raise HTTPException(status_code=500, detail="Failed to update location")

    async def delete_location(self, id: str) -> None:
        try:
            location = await self.repository.get(id)
            if not location:
                raise HTTPException(status_code=404, detail="Location not found")
            billboards = await self.billboards_repository.get_all_by_location(id)
            if len(billboards) > 0:
                raise HTTPException(status_code=409, detail="Location has billboards, update billboards first")
            await self.repository.delete(id)
        except HTTPException:
            raise
        except Exception as exc:
            logging.exception(f"Error deleting location: {exc}")
            raise HTTPException(status_code=500, detail="Failed to delete location")

    async def bulk_load_locations_from_csv(self, csv_file: IO) -> Dict[str, Any]:
        reader = csv.DictReader(csv_file)
        required_fields = {"address", "city", "state", "country_code", "lat", "lng"}
        locations_to_create = []
        errors = []
        ids = []
        for idx, row in enumerate(reader, start=2):  # start=2 to account for header row
            if not required_fields.issubset(row.keys()):
                errors.append(f"Missing required fields in CSV header.")
                break
            try:
                location_data = {
                    "address": row["address"].strip(),
                    "city": row["city"].strip(),
                    "state": row["state"].strip(),
                    "country_code": row["country_code"].strip(),
                    "lat": float(row["lat"]),
                    "lng": float(row["lng"]),
                }
                location_create = LocationCreate(**location_data)
                db_location = LocationDB(**location_create.dict())
                id = generate_prefixed_uuid("loc")
                db_location.id = id
                ids.append(id)
                locations_to_create.append(db_location)
            except Exception as exc:
                errors.append(f"Row {idx}: {exc}")
        if errors:
            return {"created": 0, "errors": errors}
        try:
            async with self.repository.session.begin():
                for db_location in locations_to_create:
                    # id will be generated by the repository/database
                    self.repository.session.add(db_location)
            return {"created": len(locations_to_create), "locations": ids, "errors": []}
        except Exception as exc:
            return {"created": 0, "errors": [f"Bulk insert failed: {exc}"]}
