# Minimal Dockerfile for the Control service (and general Python service image)
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy package and code
COPY . /app

# Generate protos at build time (optional)
RUN chmod +x ./scripts/gen_protos.sh && ./scripts/gen_protos.sh || true

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "services.control.server"]
