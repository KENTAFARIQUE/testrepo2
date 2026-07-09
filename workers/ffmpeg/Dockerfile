FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY packages/contracts /app/packages/contracts
RUN pip install -e /app/packages/contracts

COPY workers/ffmpeg/requirements.txt /app/workers/ffmpeg/requirements.txt
RUN pip install --no-cache-dir -r /app/workers/ffmpeg/requirements.txt

COPY workers/ffmpeg /app/workers/ffmpeg

CMD ["python", "-m", "workers.ffmpeg.main"]
