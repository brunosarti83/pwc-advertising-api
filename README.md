[run migrations]
poetry run alembic init migrations
poetry run alembic revision --autogenerate -m "Initial schema"
poetry run alembic upgrade head

[run production]
docker-compose up --build --detach

[run dev]
docker-compose up --build --detach redis
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
