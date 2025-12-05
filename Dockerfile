# -------------------------
# Stage 1: Builder
# -------------------------
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Copy dependency file first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# -------------------------
# Stage 2: Runtime
# -------------------------
FROM python:3.11-slim AS runtime

# Set timezone
ENV TZ=UTC
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        cron \
        tzdata \
        curl \
        ca-certificates && \
    ln -sf /usr/share/zoneinfo/UTC /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . /app

# Setup cron job (optional: you can adjust cron schedule)
# Ensure cron file has proper permissions
# Copy cron file and scripts
COPY cron/2fa-cron /etc/cron.d/2fa-cron
COPY scripts /app/scripts

# Set permissions and install cron job
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron

# Ensure cron output directory exists
RUN mkdir -p /cron && chmod 755 /cron


# Create volume mount points
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Expose FastAPI port
EXPOSE 8080

# Start cron and FastAPI server
CMD ["sh", "-c", "cron && uvicorn main:app --host 0.0.0.0 --port 8080"]
# Copy cron files
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Copy scripts
COPY scripts /app/scripts

# Set permissions and install cron job
RUN chmod 0644 /etc/cron.d/2fa-cron && \
    crontab /etc/cron.d/2fa-cron

# Ensure /cron directory exists
RUN mkdir -p /cron && chmod 755 /cron

# Start cron + FastAPI
CMD ["sh", "-c", "cron && uvicorn main:app --host 0.0.0.0 --port 8080"]
