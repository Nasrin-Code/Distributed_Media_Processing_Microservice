from app.celery_app import celery_app

@celery_app.task(bind=True)
def process_job(self, job_id: str):
    try:
        print(f"Received job: {job_id}") 
        return f"Job {job_id} acknowledged"

    except TimeoutError as error:
        print(f"Network timeout for job {job_id}: {error}")
        raise self.retry(exc=error, countdown=5)
    
    except Exception as error:
        print(f"Job {job_id} failed: {error}")
        raise