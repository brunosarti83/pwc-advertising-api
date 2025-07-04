from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from src.middleware import add_correlation_id
from src.routes.locations import router as locations_router
from src.dependencies import init_db

app = FastAPI(title="Advertising API", version="1.0.0")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Middleware
app.middleware("http")(add_correlation_id)

# Initialize DB
init_db()

# Routes
app.include_router(locations_router, prefix="/api/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/version")
async def version():
    return {"version": "1.0.0"}