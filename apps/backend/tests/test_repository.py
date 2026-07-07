import pytest

from tubedigest.repository import create_job, get_job, list_jobs, update_job


class TestCreateJob:
    async def test_creates_job_with_defaults(self, db_session):
        job = await create_job(db_session, url="https://youtube.com/watch?v=test")
        assert job.id is not None
        assert job.url == "https://youtube.com/watch?v=test"
        assert job.status == "queued"
        assert job.current_step == "queued"
        assert job.title is None
        assert job.created_at is not None
        assert job.updated_at is not None


class TestGetJob:
    async def test_returns_job_by_id(self, db_session):
        job = await create_job(db_session, url="https://youtube.com/watch?v=test")
        found = await get_job(db_session, job.id)
        assert found is not None
        assert found.id == job.id

    async def test_returns_none_for_missing_id(self, db_session):
        found = await get_job(db_session, "nonexistent-id")
        assert found is None


class TestListJobs:
    async def test_empty_list(self, db_session):
        jobs = await list_jobs(db_session)
        assert jobs == []

    async def test_returns_all_jobs(self, db_session):
        job1 = await create_job(db_session, url="https://youtube.com/watch?v=1")
        job2 = await create_job(db_session, url="https://youtube.com/watch?v=2")
        jobs = await list_jobs(db_session)
        assert len(jobs) == 2

    async def test_ordered_by_created_at_desc(self, db_session):
        job1 = await create_job(db_session, url="https://youtube.com/watch?v=1")
        job2 = await create_job(db_session, url="https://youtube.com/watch?v=2")
        jobs = await list_jobs(db_session)
        assert jobs[0].id == job2.id
        assert jobs[1].id == job1.id


class TestUpdateJob:
    async def test_updates_status(self, db_session):
        job = await create_job(db_session, url="https://youtube.com/watch?v=test")
        updated = await update_job(db_session, job.id, status="downloading")
        assert updated is not None
        assert updated.status == "downloading"

    async def test_updated_at_changes(self, db_session):
        job = await create_job(db_session, url="https://youtube.com/watch?v=test")
        original = job.updated_at
        updated = await update_job(db_session, job.id, status="downloading")
        assert updated.updated_at > original

    async def test_sets_nullable_fields(self, db_session):
        job = await create_job(db_session, url="https://youtube.com/watch?v=test")
        updated = await update_job(
            db_session, job.id,
            video_path="/storage/videos/test.mp4",
            error="something went wrong",
        )
        assert updated.video_path == "/storage/videos/test.mp4"
        assert updated.error == "something went wrong"

    async def test_returns_none_for_missing(self, db_session):
        result = await update_job(db_session, "nonexistent", status="completed")
        assert result is None
