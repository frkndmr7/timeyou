FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

COPY pyproject.toml ./
RUN pip install --no-cache-dir \
    "fastapi>=0.115,<1.0" \
    "pydantic>=2.9,<3.0" \
    "PyJWT[crypto]>=2.9,<3.0" \
    "sqlalchemy>=2.0,<3.0" \
    "psycopg[binary]>=3.2,<4.0" \
    "alembic>=1.14,<2.0" \
    "uvicorn[standard]>=0.30,<1.0" \
    "prometheus-client>=0.20,<1.0"

COPY alembic.ini ./
COPY migrations ./migrations
COPY app ./app

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
