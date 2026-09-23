# Distributed Media Processing Microservice

An event-driven backend microservice for asynchronous media processing.

## Tech Stack

- Python
- FastAPI
- Boto3
- AWS S3
- Celery
- RabbitMQ
- Redis
- Pillow
- FFmpeg

## Current Progress

### Week 1 â€” API Scaffolding & Cloud Storage
- FastAPI project structure created
- Basic FastAPI application created
- Virtual environment configured
- Requirements file created
- Git ignore configured
- AWS S3 bucket configured
- Boto3 S3 client configured
- S3 file upload and download implemented
- Automated unit tests added for S3 operations
- Pydantic job request model created
- REST API endpoint created to accept media-processing jobs
- POST /jobs endpoint tested successfully
- Redis caching layer configured for job status tracking
- Job status initialized as pending when a processing job is created
- GET /jobs/{job_id} endpoint created to retrieve job status
- 404 response implemented for unknown job IDs
- Redis job-status tests added
- Full test suite passing

## Week 2 Message Broker & Celery Workers

- RabbitMQ deployed and configured using Docker
- RabbitMQ Management UI configured
- Celery integrated into the FastAPI application
- Celery configured to use RabbitMQ as the message broker
- Celery application configuration created in `app/celery_app.py`
- Celery dependency added to `requirements.txt`
- Celery and RabbitMQ configuration verified successfully
- Existing test suite passing: 9 tests passed
- Created initial Celery worker task in `app/tasks.py`
- Registered `process_job` using the Celery task decorator
- Implemented simulated job receiving and acknowledgement
- Verified asynchronous task submission using `process_job.delay()`
- Verified RabbitMQ successfully delivers jobs to the Celery worker
- Verified Celery worker receives and executes `process_job`
- Verified successful job acknowledgement
- Full test suite passing: 9 tests passed
