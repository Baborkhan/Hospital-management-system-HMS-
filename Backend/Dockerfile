# ═══════════════════════════════════════════════════════
#  MedFind Backend — Docker Image for Google Cloud Run
# ═══════════════════════════════════════════════════════
FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc curl && \
    rm -rf /var/lib/apt/lists/*

# App directory
WORKDIR /app

# Install Python dependencies first (Docker cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY . .

# Create logs directory
RUN mkdir -p logs

# Collect static files
ENV DJANGO_SETTINGS_MODULE=config.settings.prod
RUN python manage.py collectstatic --noinput || true

# Run as non-root user (security)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Cloud Run uses PORT env variable
ENV PORT=8080
EXPOSE 8080

# Start Gunicorn
CMD exec gunicorn \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --worker-class gthread \
    --threads 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    config.wsgi:application
