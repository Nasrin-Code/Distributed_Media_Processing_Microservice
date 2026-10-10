
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.models.job import JobRequest, UploadURLRequest
from app.services.s3_service import generate_upload_url
from app.services.redis_service import (
    get_job_status,
    set_job_status,
    get_worker_cpu_usage,
)
from app.metrics import worker_cpu_usage, update_queue_length
from app.tasks import process_job

app = FastAPI()

UPLOAD_DIR = Path("/app/uploads")
ALLOWED_EXTENSIONS = {
    ".mp4", ".avi", ".mov", ".jpg", ".jpeg", ".png"
}


@app.get("/")
def home():
    return {"message": "Distributed Media Processing Microservice"}


@app.post("/upload")
async def upload_media(file: UploadFile = File(...)):
    filename = Path(file.filename or "").name

    if not filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    destination = UPLOAD_DIR / filename

    try:
        with destination.open("wb") as output:
            while chunk := await file.read(1024 * 1024):
                output.write(chunk)
    except OSError as error:
        raise HTTPException(
            status_code=500,
            detail="Could not save uploaded file",
        ) from error
    finally:
        await file.close()

    return {"filename": filename, "message": "Upload successful"}


@app.post("/jobs")
def create_job(request: JobRequest):
    job_id = str(uuid.uuid4())
    set_job_status(job_id, "pending")
    process_job.delay(job_id, request.filename, request.operation)

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

    return {"job_id": job_id, "status": status}


@app.post("/upload-url")
def create_upload_url(request: UploadURLRequest):
    object_name = f"uploads/{request.filename}"
    upload_url = generate_upload_url(object_name)

    return {"upload_url": upload_url, "object_name": object_name}


@app.get("/metrics")
def metrics():
    update_queue_length()
    worker_cpu_usage.set(get_worker_cpu_usage())

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
