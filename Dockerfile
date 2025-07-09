# Use an official Python runtime as a parent image
FROM python:3.12-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for psycopg2 and other packages
# For example, psycopg2 needs libpq-dev
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and uv.lock to leverage Docker cache
COPY pyproject.toml uv.lock ./

# Install project dependencies using uv
# uv is a fast Python package installer and resolver
RUN pip install uv && uv sync

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Define environment variables
ENV PYTHONUNBUFFERED 1

# Run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
