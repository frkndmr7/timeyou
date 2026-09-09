import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.api.routes import router as session_router
from app.api.internal_routes import router as internal_router
from app.metrics import MetricsMiddleware, metrics_response

app = FastAPI(title="Time&You Focus Service", version="0.1.0")
app.add_middleware(MetricsMiddleware)
cors_origin = os.getenv("CORS_ORIGIN")
if not cors_origin:
    raise RuntimeError("CORS_ORIGIN environment variable is required.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[cors_origin],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(session_router)
app.include_router(internal_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "focus-service", "status": "ok"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return metrics_response()
