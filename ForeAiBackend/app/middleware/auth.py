import base64
import contextlib
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse
from itsdangerous import TimestampSigner, BadSignature, SignatureExpired
from app.utils.redis_attempts import RedisAuthAttempts

EXCLUDE_PATHS = ["/health", "/static", "/favicon.ico"]

class BasicAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, security_config):
        super().__init__(app)
        self.security_config = security_config
        self.attempts = RedisAuthAttempts(security_config.redis_url)
        self.signer = TimestampSigner(security_config.session_secret)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        # Не защищаем отдельные пути
        if any(path.startswith(exclude) for exclude in EXCLUDE_PATHS):
            return await call_next(request)

        client_ip = request.client.host
        max_attempts = self.security_config.max_attempts
        max_backoff = self.security_config.max_backoff
        session_lifetime = self.security_config.session_lifetime

        # Проверка блокировки
        blocked_until = self.attempts.is_blocked(client_ip)
        now = int(time.time())
        if blocked_until > now:
            return PlainTextResponse(
                f"Too many failed attempts. Try again in {blocked_until-now} seconds.",
                status_code=429
            )

        # Проверка session cookie
        session_token = request.cookies.get("session_token")
        if session_token:
            with contextlib.suppress(BadSignature, SignatureExpired):
                self.signer.unsign(session_token, max_age=session_lifetime)
                return await call_next(request)
        # Проверка basic auth
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Basic "):
            return self._unauthorized_response()

        try:
            encoded = auth_header.split(" ")[1]
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, password = decoded.split(":", 1)
        except Exception:
            return PlainTextResponse("Invalid authorization header", status_code=400)

        if (
            username != self.security_config.USER
            or password != self.security_config.PASSWORD
        ):
            backoff = self.attempts.record_failure(client_ip, max_attempts, max_backoff)
            if backoff:
                return PlainTextResponse(
                    f"Too many failed attempts. Blocked for {int(backoff)} seconds.",
                    status_code=429
                )
            return self._unauthorized_response()

        # Успех — сброс попыток
        self.attempts.reset(client_ip)
        # Сессия
        session_token = self.signer.sign(str(client_ip)).decode()
        response = await call_next(request)
        response.set_cookie(
            "session_token",
            session_token,
            max_age=session_lifetime,
            httponly=True,
            samesite="strict",
            secure=True,    # Для HTTPS!
        )
        return response

    def _unauthorized_response(self):
        return Response(
            status_code=401,
            headers={"WWW-Authenticate": "Basic"},
            content="Unauthorized"
        )
