import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.persistence.models import Location
from sqlmodel import Session, SQLModel, create_engine
from src.dependencies import get_db, get_db_engine

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_create_location(client, db_session, monkeypatch):
    def mock_get_db():
        yield db_session
    monkeypatch.setattr("src.dependencies.get_db", mock_get_db)
    
    response = client.post("/api/v1/locations", json={
        "address": "123 Main St",
        "city": "NYC",
        "state": "NY",
        "country_code": "US",
        "lat": 40.7128,
        "lng": -74.0060
    }, headers={"Authorization": "Bearer mock-jwt"})
    assert response.status_code == 201
    assert response.json()["id"].startswith("loc_")