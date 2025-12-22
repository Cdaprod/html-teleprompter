# Dev container for the teleprompter FastAPI service
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TELEPROMPTER_HOST=${TELEPROMPTER_HOST:-0.0.0.0} \
    TELEPROMPTER_PORT=${TELEPROMPTER_PORT:-8790} \
    TELEPROMPTER_PROJECTS_ROOT=${TELEPROMPTER_PROJECTS_ROOT:-/data/projects} \
    TELEPROMPTER_CORS_ORIGINS=${TELEPROMPTER_CORS_ORIGINS:-*}

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8790

CMD ["sh", "-c", "uvicorn app.main:app --host ${TELEPROMPTER_HOST:-0.0.0.0} --port ${TELEPROMPTER_PORT:-8790} --reload"]
