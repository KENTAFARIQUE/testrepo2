import pytest
from httpx import AsyncClient, ASGITransport

from tubedigest.database import get_db
from tubedigest.dependencies import get_publisher
from tubedigest.main import app
from tubedigest.publisher import FakePublisher


@pytest.fixture(autouse=True)
def override_deps(db_session, fake_publisher):
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_publisher] = lambda: fake_publisher
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def fake_publisher():
    return FakePublisher()


class TestPostVideos:
    async def test_valid_url_returns_201(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post("/videos", json={"url": "https://youtube.com/watch?v=test"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["url"] == "https://youtube.com/watch?v=test"
        assert data["status"] == "queued"
        assert data["current_step"] == "queued"
        assert "id" in data
        assert "created_at" in data

    async def test_publishes_video_download_message(self, fake_publisher):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            await client.post("/videos", json={"url": "https://youtube.com/watch?v=test"})
        assert len(fake_publisher.published_messages) == 1
        queue, msg = fake_publisher.published_messages[0]
        assert queue == "video.download"
        assert msg.url == "https://youtube.com/watch?v=test"
        assert msg.attempt == 1

    async def test_empty_url_returns_422(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post("/videos", json={"url": ""})
        assert resp.status_code == 422

    async def test_db_has_job_after_post(self, db_session):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post("/videos", json={"url": "https://youtube.com/watch?v=test"})
        job_id = resp.json()["id"]
        from tubedigest.repository import get_job
        job = await get_job(db_session, job_id)
        assert job is not None
        assert job.status == "queued"


class TestGetVideos:
    async def test_empty_list(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get("/videos")
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_returns_jobs_ordered_by_created_at_desc(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            r1 = await client.post("/videos", json={"url": "https://youtube.com/watch?v=1"})
            r2 = await client.post("/videos", json={"url": "https://youtube.com/watch?v=2"})
            resp = await client.get("/videos")
        data = resp.json()
        assert len(data) == 2
        assert data[0]["id"] == r2.json()["id"]
        assert data[1]["id"] == r1.json()["id"]

    async def test_returns_job_by_id(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            created = await client.post("/videos", json={"url": "https://youtube.com/watch?v=test"})
            job_id = created.json()["id"]
            resp = await client.get(f"/videos/{job_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == job_id
        assert resp.json()["url"] == "https://youtube.com/watch?v=test"

    async def test_returns_404_for_unknown_id(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get("/videos/nonexistent-id")
        assert resp.status_code == 404
