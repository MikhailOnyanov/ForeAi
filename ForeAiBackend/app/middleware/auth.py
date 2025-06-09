import base64
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse
from app.configuration import SecurityConfig

class BasicAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, security_config: SecurityConfig):
        super().__init__(app)
        self.security_config = security_config

    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Basic "):
            return Response(
                status_code=401,
                headers={"WWW-Authenticate": "Basic"},
                content="Unauthorized"
            )

        encoded = auth_header.split(" ")[1]
        try:
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, password = decoded.split(":", 1)
        except Exception:
            return PlainTextResponse("Invalid authorization header", status_code=400)

        if (
            username != self.security_config.USER
            or password != self.security_config.PASSWORD
        ):
            return Response(
                status_code=401,
                headers={"WWW-Authenticate": "Basic"},
                content="Unauthorized"
            )

        return await call_next(request)
