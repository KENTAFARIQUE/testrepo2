FROM python:3.12-slim

WORKDIR /app

COPY packages/contracts /app/packages/contracts
RUN pip install -e /app/packages/contracts

COPY workers/summary/requirements.txt /app/workers/summary/requirements.txt
RUN pip install --no-cache-dir -r /app/workers/summary/requirements.txt

COPY workers/summary /app/workers/summary

CMD ["python", "-m", "workers.summary.main"]
