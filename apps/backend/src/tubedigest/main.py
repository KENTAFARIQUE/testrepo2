from fastapi import FastAPI

from tubedigest.routers.videos import router as videos_router

app = FastAPI(title="TubeDigest API", version="0.1.0")
app.include_router(videos_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
