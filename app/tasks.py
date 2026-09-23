from app.celery_app import celery_app

@celery_app.task
def process_job(job_id: str):
    print(f"Received job: {job_id}")
    return f"Job {job_id} acknowledged"