from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import uuid
import time

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = request_id

        start = time.perf_counter()
        response: Response = await call_next(request)
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        response.headers["x-request-id"] = request_id
        response.headers["x-elapsed-ms"] = str(elapsed_ms)
        return response
