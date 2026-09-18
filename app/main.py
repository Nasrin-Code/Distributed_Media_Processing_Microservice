from fastapi import FastAPI

from app.models.job import JobRequest

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