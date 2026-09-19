from fastapi import FastAPI

from app.models.job import JobRequest, UploadURLRequest
from app.services.s3_service import generate_upload_url

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Distributed Media Processing Microservice"}

@app.post("/jobs")
def create_job(request: JobRequest):
    return{
        "filename": request.filename,
        "operation": request.operation
          }

@app.post("/upload-url")
def create_upload_url(request: UploadURLRequest):
    object_name = f"uploads/{request.filename}"
    upload_url = generate_upload_url(object_name)
    return {"upload_url": upload_url, "object_name": object_name}