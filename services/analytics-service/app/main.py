import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as analytics_router

app = FastAPI(title="Time&You Analytics Service", version="0.1.0")
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
app.include_router(analytics_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "analytics-service", "status": "ok"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
