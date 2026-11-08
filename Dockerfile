FROM python:3.14.8 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app


RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install -r requirements.txt
FROM python:3.14.8-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .
ENV PYTHONPATH=/app

EXPOSE 8000
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "8000"]
