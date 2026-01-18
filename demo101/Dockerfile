#Use official Python runtime as base image
# python:3.11-slim is smaller and more secure than full python:3.11
FROM python:3.11-slim

# Set metadata labels -optional parameters
LABEL maintainer="docker-class@example.com"
LABEL version="1.0.0"
LABEL description="Simple Flask app for Docker class demonstration"

# Set environment variables - Optional but depends on your app needs
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
# Set application environment
ENV APP_ENV=production
# Set default port
ENV PORT=5000

# Set working directory in container
WORKDIR /app

# Install system dependencies (if needed)
# This step is optional for this simple app, but good practice
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first (for better caching)
# Docker caches layers, so if requirements don't change,
# it won't reinstall packages on every build
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create non-root user for security
# Running as root in containers is a security risk
RUN useradd -m -u 1000 flaskuser && \
    chown -R flaskuser:flaskuser /app

# Switch to non-root user
USER flaskuser

# Expose port that the app runs on

EXPOSE 5000

# Health check - Docker will check if container is healthy
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Command to run the application
# Using exec form (JSON array) for proper signal handling
CMD ["python", "app.py"]

