import os

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response


async def verify_frontend(request: Request):
    if os.name == "nt":
        return True

    if request.headers.get("frontend-call"):
        return True
    else:
        raise HTTPException(status_code=403, detail="Url reserved for backend only.")


class VerifyFrontendMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            await verify_frontend(request)
            return await call_next(request)
        except HTTPException as e:
            return Response(e.detail, status_code=e.status_code)
        except Exception as e:
            return Response(str(e), status_code=500)
