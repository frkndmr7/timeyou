import asyncio
import os
import unittest

os.environ.setdefault("CORS_ORIGIN", "http://localhost:3001")

from app.main import app  # noqa: E402


async def request(path: str) -> tuple[int, bytes, str]:
    messages: list[dict] = []

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: dict) -> None:
        messages.append(message)

    await app(
        {
            "type": "http",
            "http_version": "1.1",
            "method": "GET",
            "path": path,
            "raw_path": path.encode(),
            "query_string": b"",
            "headers": [],
            "scheme": "http",
            "server": ("test", 80),
            "client": ("test", 1),
        },
        receive,
        send,
    )
    status = next(message["status"] for message in messages if message["type"] == "http.response.start")
    headers = dict(next(message["headers"] for message in messages if message["type"] == "http.response.start"))
    body = b"".join(message.get("body", b"") for message in messages)
    return status, body, headers[b"content-type"].decode()


class MetricsTests(unittest.TestCase):
    def test_metrics_endpoint_is_public_and_excluded_from_request_metrics(self) -> None:
        status, body, content_type = asyncio.run(request("/metrics"))
        self.assertEqual(status, 200)
        self.assertTrue(content_type.startswith("text/plain"))
        self.assertIn(b"timeyou_http_requests_total", body)
        self.assertNotIn(b'route="/metrics"', body)

    def test_request_metrics_use_templated_routes(self) -> None:
        status, _, _ = asyncio.run(request("/analytics/summary"))
        self.assertEqual(status, 401)
        _, body, _ = asyncio.run(request("/metrics"))
        self.assertIn(b'route="/analytics/summary"', body)
