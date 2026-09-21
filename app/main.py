import uuid

from fastapi import FastAPI, HTTPException

from app.models.job import JobRequest, UploadURLRequest
from app.services.s3_service import generate_upload_url
from app.services.redis_service import get_job_status, set_job_status

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Distributed Media Processing Microservice"}


@app.post("/jobs")
def create_job(request: JobRequest):
    job_id = str(uuid.uuid4())

    set_job_status(job_id, "pending")

    return {
        "job_id": job_id,
        "filename": request.filename,
        "operation": request.operation,
        "status": "pending",
    }


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = get_job_status(job_id)

    if status is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job_id,
        "status": status,
    }


@app.post("/upload-url")
def create_upload_url(request: UploadURLRequest):
    object_name = f"uploads/{request.filename}"
    upload_url = generate_upload_url(object_name)

    return {
        "upload_url": upload_url,
        "object_name": object_name,
    }