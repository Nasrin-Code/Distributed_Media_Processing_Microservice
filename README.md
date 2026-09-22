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

### Week 1 — API Scaffolding & Cloud Storage
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

## Week 2 — Message Broker & Celery Workers

### Day 1–3
- RabbitMQ deployed and configured using Docker
- RabbitMQ Management UI configured
- Celery integrated into the FastAPI application
- Celery configured to use RabbitMQ as the message broker
- Celery application configuration created in `app/celery_app.py`
- Celery dependency added to `requirements.txt`
- Celery and RabbitMQ configuration verified successfully
- Existing test suite passing: 9 tests passed