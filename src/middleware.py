from fastapi import Request, Response
from slowapi import Limiter
from starlette.middleware.base import BaseHTTPMiddleware
import uuid

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = str(uuid.uuid4())
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response

async def add_correlation_id(request: Request, call_next):
    return await CorrelationIdMiddleware(app=None).dispatch(request, call_next)