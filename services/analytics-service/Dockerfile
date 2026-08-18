FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir \
    "fastapi>=0.115,<1.0" \
    "httpx>=0.27,<1.0" \
    "pydantic>=2.9,<3.0" \
    "PyJWT[crypto]>=2.9,<3.0" \
    "uvicorn[standard]>=0.30,<1.0"

COPY app ./app

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
