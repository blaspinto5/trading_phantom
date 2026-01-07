# Dockerfile (backtesting & API only, no MT5 / no GUI)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements-docker.txt /app/requirements-docker.txt
RUN pip install --no-cache-dir -r /app/requirements-docker.txt

# Copy source
COPY src /app/src
COPY docs /app/docs
COPY Readme.md /app/Readme.md

EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import requests; print(requests.get('http://localhost:5000/api/bot/status').status_code)" || exit 1

# Start Flask webapp
CMD ["python", "-m", "trading_phantom.webapp"]
