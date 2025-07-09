FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
COPY src ./src
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --only main
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]