from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tubedigest.routers.videos import router as videos_router
from tubedigest.settings import settings

origins = [o.strip() for o in settings.cors_origins.split(",")]

app = FastAPI(title="TubeDigest API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(videos_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
