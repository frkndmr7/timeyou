from collections.abc import Awaitable, Callable
from time import perf_counter

from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response


REQUESTS = Counter(
    "timeyou_http_requests",
    "Total HTTP requests handled by the service.",
    ("method", "route", "status"),
)
REQUEST_DURATION = Histogram(
    "timeyou_http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ("method", "route", "status"),
)


def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


class MetricsMiddleware:
    def __init__(self, app: Callable[..., Awaitable[None]]) -> None:
        self.app = app

    async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
        if scope.get("type") != "http" or scope.get("path") == "/metrics":
            await self.app(scope, receive, send)
            return

        status_code = 500

        async def send_wrapper(message: dict) -> None:
            nonlocal status_code
            if message.get("type") == "http.response.start":
                status_code = message["status"]
            await send(message)

        started = perf_counter()
        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            route = getattr(scope.get("route"), "path", None) or "<unmatched>"
            labels = (scope.get("method", "UNKNOWN"), route, str(status_code))
            REQUESTS.labels(*labels).inc()
            REQUEST_DURATION.labels(*labels).observe(perf_counter() - started)
