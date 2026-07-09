import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tubedigest.database import Base, engine
from tubedigest.models import VideoJob  # noqa: F401
from tubedigest.routers.videos import router as videos_router
from tubedigest.settings import settings
from tubedigest.sse import sse_manager, start_consumer

origins = [o.strip() for o in settings.cors_origins.split(",")]

_consumer_thread = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _consumer_thread
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    if not settings.use_fake_publisher:
        loop = asyncio.get_running_loop()
        _consumer_thread = start_consumer(loop, sse_manager, settings.rabbitmq_url)

    yield


app = FastAPI(title="TubeDigest API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(videos_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}
