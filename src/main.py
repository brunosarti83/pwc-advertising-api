from fastapi import FastAPI, Request
from slowapi import _rate_limit_exceeded_handler
from src.routes.locations import router as locations_router
from src.routes.billboards import router as billboards_router
from src.routes.campaigns import router as campaigns_router
from src.routes.auth import router as auth_router
from src.limiter import limiter

app = FastAPI(title="Advertising API", version="1.0.0")

# Limiter setup
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Routes
app.include_router(auth_router, prefix="/api/v1")
app.include_router(locations_router, prefix="/api/v1")
app.include_router(billboards_router, prefix="/api/v1")
app.include_router(campaigns_router, prefix="/api/v1")

@app.get("/health")
@limiter.limit("100/minute")
async def health(request: Request):
    return {"status": "ok"}

@app.get("/version")
@limiter.limit("100/minute")
async def version(request: Request):
    return {"version": "1.0.0"}