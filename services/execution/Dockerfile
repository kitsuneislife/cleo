FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN chmod +x ./scripts/gen_protos.sh && ./scripts/gen_protos.sh || true
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "services.execution.server"]
