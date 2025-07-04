FROM python:3.12-alpine

WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry && poetry install --no-dev
COPY src /app/src
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]