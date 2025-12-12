# Docker boilerplate

# Build stage: Install poetry and build venv
FROM python:3.13-slim as builder

# Change this to current service dir name
ENV SERVICE_DIR=api_gateway

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Update apt and clear cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry>=2.0.0"

WORKDIR /project

# Copy shared models
COPY shared/ /project/shared/

# Copy poetry dependencies
COPY ${SERVICE_DIR}/pyproject.toml ${SERVICE_DIR}/poetry.lock* /project/${SERVICE_DIR}/

# Install dependencies
WORKDIR /project/${SERVICE_DIR}
RUN poetry install --no-root --only main

# Runtime stage: Copy code
FROM python:3.13-slim as runtime

ENV VIRTUAL_ENV=/project/${SERVICE_DIR}/.venv \
    PATH="/project/${SERVICE_DIR}/.venv/bin:$PATH"

WORKDIR /app

# Install runtime dependencies and clear cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

#Copy venv from the builder stage
COPY --from=builder /project/${SERVICE_DIR}/.venv /project/${SERVICE_DIR}/.venv

# Copy application code
COPY ${SERVICE_DIR}/ /app/

# Code to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
