from src.persistence.models import Location as LocationDB
from src.persistence.repositories import LocationRepository
from src.domain.models import Location, LocationCreate, LocationUpdate
from sqlmodel import Session
from fastapi import HTTPException
from typing import List

class LocationService:
    def __init__(self, session: Session):
        self.repository = LocationRepository(LocationDB, session)

    def create_location(self, location: LocationCreate) -> Location:
        db_location = LocationDB(**location.dict())
        created = self.repository.create(db_location)
        return Location(**created.dict(), links={"self": f"/api/v1/locations/{created.id}"})

    def get_location(self, id: str) -> Location:
        location = self.repository.get(id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        return Location(**location.dict(), links={"self": f"/api/v1/locations/{id}"})

    def get_locations(self, offset: int = 0, limit: int = 100) -> List[Location]:
        locations = self.repository.get_all(offset, limit)
        return [Location(**loc.dict(), links={"self": f"/api/v1/locations/{loc.id}"}) for loc in locations]

    def delete_location(self, id: str) -> None:
        location = self.repository.get(id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        self.repository.delete(id)