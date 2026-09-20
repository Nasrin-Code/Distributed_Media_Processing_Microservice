from app.services.redis_service import get_job_status, set_job_status

def test_set_and_get_job_status():
    job_id = "test-job-001"
    set_job_status(job_id, "pending")
    assert get_job_status(job_id) == "pending"

def test_get_missing_job_status():
    job_id = "job-that-does-not-exist"
    assert get_job_status(job_id) is None