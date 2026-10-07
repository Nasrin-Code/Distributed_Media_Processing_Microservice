# Distributed Media Processing Microservice

## 2nd Month Internship Project — Mid-Review Report

**Organization:** Zaalima Development Pvt. Ltd.  
**Project:** Distributed Media Processing Microservice  
**Developer:** Nasrin A  
**Programming Language:** Python  
**Framework:** FastAPI  
**Current Progress:** Week 4 — Metrics, Deployment Documentation, Load Testing and Memory Analysis

---

## 1. Project Overview

The Distributed Media Processing Microservice is a Python-based backend system designed to process media files through distributed background jobs.

The project uses FastAPI to expose REST API endpoints, Amazon S3 for presigned upload URLs, Redis for job-status storage, Celery for asynchronous background processing, RabbitMQ as the message broker, FFmpeg for video processing, Pillow for image processing, and Prometheus-compatible metrics for monitoring.

The application is containerized using Docker Compose and is organized into separate API, worker, Redis, and RabbitMQ services.

The project is developed incrementally with modular service components, automated testing, background task processing, monitoring, and deployment documentation.

---

## 2. Project Objectives

- Develop REST API endpoints using FastAPI.
- Implement image and video media-processing operations.
- Integrate Amazon S3 presigned URLs for media uploads.
- Use Redis to track processing job statuses.
- Use Celery for asynchronous background processing.
- Use RabbitMQ as the Celery message broker.
- Implement FFmpeg-based video processing.
- Implement Pillow-based image processing.
- Add Prometheus-compatible monitoring metrics.
- Containerize the application using Docker Compose.
- Write automated tests using Pytest.
- Perform load testing and memory-usage analysis.
- Build a distributed media-processing workflow.

---

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | Backend REST API framework |
| Uvicorn | ASGI application server |
| Pydantic | Request validation and data models |
| Pillow | Image processing |
| FFmpeg | Video thumbnail extraction and transcoding |
| Amazon S3 / Boto3 | Object storage and presigned upload URLs |
| Redis | Job-status and worker metric storage |
| Celery | Asynchronous background task processing |
| RabbitMQ | Message broker for Celery |
| Prometheus Client | Application metrics |
| psutil | Worker CPU monitoring |
| Pytest | Automated testing |
| HTTPX | API testing support |
| Docker | Containerization |
| Docker Compose | Multi-service local deployment |
| Git and GitHub | Version control and source-code hosting |

---

## 4. Project Architecture

The application follows a distributed service architecture:

```text
                         Client
                           |
                           v
                    +-------------+
                    |   FastAPI   |
                    |     API     |
                    +-------------+
                      |    |    |
             +--------+    |    +--------+
             |             |             |
             v             v             v
          Redis        RabbitMQ        Amazon S3
       Job Status      Message Broker   File Storage
                          |
                          v
                    +-------------+
                    |   Celery    |
                    |   Worker     |
                    +-------------+
                          |
                 +--------+--------+
                 |                 |
                 v                 v
              FFmpeg            Pillow
           Video Processing   Image Processing
```

### Docker Services

The Docker Compose environment contains four services:

- **API** — FastAPI application.
- **Worker** — Celery background worker.
- **RabbitMQ** — Message broker.
- **Redis** — Job-status and metric storage.

---

## 5. Project Structure

```text
Distributed_Media_Processing_Microservice/
│
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   └── job.py
│   │
│   ├── services/
│   │   ├── image_service.py
│   │   ├── redis_service.py
│   │   ├── s3_service.py
│   │   └── video_service.py
│   │
│   ├── __init__.py
│   ├── celery_app.py
│   ├── main.py
│   ├── metrics.py
│   └── tasks.py
│
├── tests/
│   ├── test_image_service.py
│   ├── test_main.py
│   ├── test_redis_service.py
│   ├── test_s3_service.py
│   └── test_video_service.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 6. Implemented Components

### 6.1 FastAPI Application

FastAPI is used to provide the REST API.

Implemented endpoints include:

- `GET /` — returns the application message.
- `POST /jobs` — creates a media-processing job.
- `GET /jobs/{job_id}` — retrieves the current status of a job.
- `POST /upload-url` — generates a presigned S3 upload URL.
- `GET /metrics` — exposes Prometheus-compatible application metrics.

Pydantic models are used to validate job and upload requests.

---

### 6.2 Job Creation and Status Tracking

When a new job is created:

1. A unique job ID is generated.
2. The initial status is stored in Redis as `pending`.
3. The job is submitted to Celery.
4. Celery sends the task through RabbitMQ.
5. The worker changes the status to `processing`.
6. The requested media operation is executed.
7. The final status becomes `completed`.
8. If an error occurs, the status becomes `failed`.

Supported job-status values include:

```text
pending
processing
completed
failed
```

---

### 6.3 Celery Background Processing

Celery is used to execute media-processing jobs asynchronously.

The API does not perform the processing directly. Instead, it submits a task to Celery:

```text
FastAPI
   |
   v
Celery
   |
   v
RabbitMQ
   |
   v
Celery Worker
   |
   v
Media Processing
```

This allows the API to remain responsive while media-processing operations are performed by the worker.

---

### 6.4 RabbitMQ

RabbitMQ is used as the message broker for Celery.

It manages messages between the FastAPI application and the Celery worker.

Docker Compose provides RabbitMQ with:

```text
AMQP: 5672
Management UI: 15672
```

---

### 6.5 Redis Job Status

Redis is used to store job statuses.

The application stores values using job-specific Redis keys:

```text
job:<job_id>
```

Redis is also used to store the latest worker CPU usage.

---

### 6.6 Amazon S3 Integration

The S3 service generates presigned upload URLs.

The upload endpoint creates an object name using the `uploads/` prefix.

Example:

```text
uploads/video.mp4
```

This allows clients to upload media directly to object storage without transferring the media file through the FastAPI application.

---

### 6.7 Pillow Image Processing

Pillow is used for image-processing operations.

Implemented operations include:

- Image cropping
- Image resizing
- JPEG image compression

The image-processing service is organized separately from the API and background-task logic.

---

### 6.8 FFmpeg Video Processing

FFmpeg is used for video-processing operations.

Implemented operations include:

**Thumbnail extraction**

Extracts a video frame at a specified timestamp and saves it as an image.

**Video transcoding**

Converts video using H.264 video encoding and AAC audio encoding.

The worker executes these operations as background Celery tasks.

---

## 7. Prometheus Metrics

A Prometheus-compatible `/metrics` endpoint has been implemented.

The application exposes:

### Queue Length

```text
queue_length
```

Tracks the number of jobs waiting in the Celery queue.

### Worker CPU Usage

```text
worker_cpu_usage
```

Tracks worker CPU usage percentage.

Example:

```text
# HELP queue_length Number of jobs waiting in the queue
# TYPE queue_length gauge
queue_length 0.0

# HELP worker_cpu_usage CPU usage percentage of the worker
# TYPE worker_cpu_usage gauge
worker_cpu_usage 1.2
```

The metrics endpoint can be accessed at:

```text
http://localhost:8000/metrics
```

---

## 8. Docker Deployment

The complete application can be started using Docker Compose.

### Build and start the services

```powershell
docker compose up --build
```

This starts:

- FastAPI API
- Celery worker
- RabbitMQ
- Redis

### Check running services

```powershell
docker compose ps
```

All four services should show a running status.

### Stop the services

```powershell
docker compose down
```

---

## 9. API Verification

The root endpoint was verified after starting the Docker environment.

Request:

```text
GET http://localhost:8000/
```

Response:

```json
{
  "message": "Distributed Media Processing Microservice"
}
```

The endpoint returned:

```text
HTTP 200 OK
```

confirming that the FastAPI service was running correctly inside Docker.

---

## 10. Testing and Validation

Pytest is used for automated testing.

The current test suite contains tests covering:

- Image processing
- FastAPI endpoints
- Redis services
- S3 services
- Video processing

The complete test suite was executed inside the Docker API container.

Latest result:

```text
18 passed, 1 warning
```

The warning is related to a testing dependency deprecation and does not represent a test failure.

---

## 11. Load Testing

A basic API load test was performed against the root endpoint.

Command:

```powershell
1..50 | ForEach-Object {
    Invoke-WebRequest -UseBasicParsing http://localhost:8000/
}
```

### Result

The API successfully processed the 50 requests.

All observed responses returned:

```text
StatusCode : 200
```

with the expected application response:

```json
{
  "message": "Distributed Media Processing Microservice"
}
```

### Load Test Conclusion

The basic API endpoint successfully handled 50 sequential requests without HTTP failures during the local Docker test.

This was a basic functional load test rather than a production-scale performance benchmark.

---

## 12. Memory Usage Analysis

Docker container memory usage was measured using:

```powershell
docker stats --no-stream
```

Measured baseline:

| Service | Memory Usage |
|---|---:|
| Celery Worker | 44.89 MiB |
| FastAPI API | 69.14 MiB |
| RabbitMQ | 160.1 MiB |
| Redis | 9.09 MiB |

The containers were operating within the available Docker memory limit.

### Memory Optimization Conclusion

The baseline measurement did not indicate an immediate memory-consumption problem.

Therefore, no unnecessary code-level memory optimization was introduced.

The measured memory values are recorded as the baseline for future performance monitoring and optimization.

---

## 13. Local Development Environment

The project was developed and tested using:

- Windows 11
- Visual Studio Code
- Python virtual environment
- PowerShell
- Docker
- Docker Compose
- Git
- GitHub

Supporting services are run through Docker Compose.

---

## 14. Current Project Status

### Completed

- FastAPI REST API
- Pydantic request models
- Amazon S3 presigned upload URL generation
- Redis job-status storage
- Celery background processing
- RabbitMQ message broker
- Pillow image processing
- FFmpeg video processing
- Docker Compose environment
- Prometheus-compatible metrics endpoint
- Queue-length monitoring
- Worker CPU monitoring
- Automated test suite
- Docker-based test verification
- Basic API load testing
- Memory usage measurement
- Deployment documentation

### Current Validation

```text
Docker services: Running
API verification: Passed
Load test: 50/50 successful HTTP responses
Automated tests: 18 passed
Metrics endpoint: Verified
Memory baseline: Measured
```

---

## 15. Repository

**GitHub:**

https://github.com/Nasrin-Code/Distributed_Media_Processing_Microservice

The repository contains the application source code, automated tests, Docker configuration, dependency configuration, and project documentation.

---

## 16. Conclusion

The Distributed Media Processing Microservice has progressed from a basic FastAPI backend into a distributed, containerized media-processing system.

The current implementation combines:

- FastAPI for API services
- Celery for asynchronous processing
- RabbitMQ for task messaging
- Redis for job-status storage
- Pillow for image processing
- FFmpeg for video processing
- Amazon S3 for media upload integration
- Prometheus-compatible metrics for monitoring
- Docker Compose for multi-service deployment

The application has been validated through automated testing, API verification, basic load testing, metrics verification, and memory-usage analysis.