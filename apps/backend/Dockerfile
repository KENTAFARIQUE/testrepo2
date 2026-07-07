FROM python:3.12-slim

WORKDIR /app

COPY packages/contracts /app/packages/contracts
RUN pip install -e /app/packages/contracts

COPY apps/backend/pyproject.toml /app/apps/backend/
RUN pip install -e /app/apps/backend

COPY apps/backend/src /app/apps/backend/src

WORKDIR /app/apps/backend
EXPOSE 8000

CMD ["uvicorn", "tubedigest.main:app", "--host", "0.0.0.0", "--port", "8000"]
