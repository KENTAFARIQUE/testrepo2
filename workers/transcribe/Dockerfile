FROM python:3.12-slim

WORKDIR /app

COPY packages/contracts /app/packages/contracts
RUN pip install -e /app/packages/contracts

COPY workers/transcribe/requirements.txt /app/workers/transcribe/requirements.txt
RUN pip install --no-cache-dir -r /app/workers/transcribe/requirements.txt

COPY workers/transcribe /app/workers/transcribe

CMD ["python", "-m", "workers.transcribe.main"]
