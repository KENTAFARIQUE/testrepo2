FROM python:3.12-slim

WORKDIR /app

COPY packages/contracts /app/packages/contracts
RUN pip install -e /app/packages/contracts

COPY workers/tags/requirements.txt /app/workers/tags/requirements.txt
RUN pip install --no-cache-dir -r /app/workers/tags/requirements.txt

COPY workers/tags /app/workers/tags

CMD ["python", "-m", "workers.tags.main"]
