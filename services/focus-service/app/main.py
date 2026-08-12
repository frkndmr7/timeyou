from fastapi import FastAPI

app = FastAPI(title="Time&You Focus Service", version="0.1.0")


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "focus-service", "status": "ok"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
