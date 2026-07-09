FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates \
    && update-ca-certificates --fresh \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY packages/contracts /app/packages/contracts
RUN pip install -e /app/packages/contracts

COPY workers/ytd/requirements.txt /app/workers/ytd/requirements.txt
RUN pip install --no-cache-dir -r /app/workers/ytd/requirements.txt

COPY workers/ytd /app/workers/ytd

CMD ["python", "-m", "workers.ytd.main"]
