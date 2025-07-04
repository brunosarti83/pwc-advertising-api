from sqlmodel import Session, select
from typing import Generic, TypeVar, Type, Optional, List
from src.persistence.models import Location
from src.utils.uuid import generate_prefixed_uuid

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def create(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get(self, id: str) -> Optional[T]:
        statement = select(self.model).where(self.model.id == id, self.model.is_deleted == False)
        return self.session.exec(statement).first()

    def get_all(self, offset: int = 0, limit: int = 100) -> List[T]:
        statement = select(self.model).where(self.model.is_deleted == False).offset(offset).limit(limit)
        return self.session.exec(statement).all()

    def delete(self, id: str) -> None:
        obj = self.get(id)
        if obj:
            obj.is_deleted = True
            self.session.add(obj)
            self.session.commit()

class LocationRepository(BaseRepository[Location]):
    def create(self, obj: Location) -> Location:
        obj.id = generate_prefixed_uuid("loc")
        return super().create(obj)