# --- Stage 1: The Builder ---
FROM python:3.11-alpine as builder

# Set build directory
WORKDIR /usr/src/app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies needed to compile some Python packages
RUN apk add --no-cache gcc musl-dev libffi-dev

# Upgrade pip and install requirements into a 'wheels' directory
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


# --- Stage 2: The Final Runtime ---
FROM python:3.11-alpine

# Create a non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set the working directory
WORKDIR /app

# Copy the compiled wheels from the builder stage
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

# Install the wheels (no compilers needed here!)
RUN pip install --no-cache /wheels/*

# Copy your application code
COPY . .

# Change ownership of the app folder to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]
