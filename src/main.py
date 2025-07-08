from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from src.error_handlers import generic_exception_handler
from src.limiter import limiter
from src.routes.auth import router as auth_router
from src.routes.availability import router as availability_router
from src.routes.billboards import router as billboards_router
from src.routes.campaigns import router as campaigns_router
from src.routes.locations import router as locations_router

app = FastAPI(title="Advertising API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Limiter setup
app.state.limiter = limiter

# Exception handlers
app.add_exception_handler(429, _rate_limit_exceeded_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Routes
app.include_router(auth_router, prefix="/api/v1")
app.include_router(locations_router, prefix="/api/v1")
app.include_router(billboards_router, prefix="/api/v1")
app.include_router(campaigns_router, prefix="/api/v1")
app.include_router(availability_router, prefix="/api/v1")

@app.get("/health")
@limiter.limit("100/minute")
async def health(request: Request):
    return {"status": "ok"}

@app.get("/version")
@limiter.limit("100/minute")
async def version(request: Request):
    return {"version": "1.0.0"}

