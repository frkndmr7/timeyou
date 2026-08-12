from fastapi import FastAPI

app = FastAPI(title="Time&You Analytics Service", version="0.1.0")


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "analytics-service", "status": "ok"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
