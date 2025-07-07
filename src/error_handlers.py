from fastapi import Request
from fastapi.responses import JSONResponse
import logging

async def generic_exception_handler(request: Request, exc: Exception):
    logging.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please contact support if this persists."}
    )
