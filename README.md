# Distributed Media Processing Microservice

**Organization:** Zaalima Development Pvt. Ltd.  
**Project:** Distributed Media Processing Microservice  
**Developer:** Nasrin A  
**Programming Language:** Python  
**Framework:** FastAPI  
**Current Progress:** Metrics, Deployment Documentation, Load Testing, Memory Analysis, and Optional Frontend Enhancement

---

## 1. Project Overview

The Distributed Media Processing Microservice is a Python-based backend application designed to process media files through distributed background jobs.

The project uses FastAPI to expose REST API endpoints, Amazon S3 for presigned upload URLs, Redis for job-status storage, Celery for asynchronous background processing, RabbitMQ as the message broker, FFmpeg for video processing, Pillow for image processing, and Prometheus-compatible metrics for monitoring.

The application is containerized using Docker Compose and is organized into separate API, worker, Redis, and RabbitMQ services.

An optional Streamlit frontend provides a user interface for uploading videos, submitting processing jobs, and checking job status.

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
- Perform basic API load testing and memory-usage analysis.
- Build a distributed media-processing workflow.
- Provide an optional Streamlit frontend for interacting with the backend.

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
| psutil | CPU usage monitoring |
| Pytest | Automated testing |
| HTTPX | API testing support |
| Docker | Containerization |
| Docker Compose | Multi-service deployment |
| Streamlit | Optional frontend interface |
| Requests | HTTP communication between frontend and backend |
| Git and GitHub | Version control and source-code hosting |

## 4. Project Architecture

The application follows a distributed service architecture.

```text
                         Client
                           |
                           v
                    +-------------+
                    |  Streamlit  |
                    |  (Optional) |
                    +-------------+
                           |
                           v
                    +-------------+
                    |   FastAPI   |
                    |     API     |
                    +-------------+
                      |    |    |
              +-------+    |    +--------+
              |            |             |
              v            v             v
            Redis       RabbitMQ     Amazon S3
          Job Status   Message Broker  Object Storage
                           |
                           v
                    +-------------+
                    | Celery      |
                    | Worker      |
                    +-------------+
                           |
                  +--------+--------+
                  |                 |
                  v                 v
               FFmpeg            Pillow
          Video Processing   Image Processing
```

### Docker Services

The Docker Compose environment contains four backend services:

- **API:** FastAPI application that exposes REST endpoints.
- **Worker:** Celery background worker that executes media-processing jobs.
- **RabbitMQ:** Message broker that transports tasks to the worker.
- **Redis:** Stores job statuses and worker CPU usage.

The optional Streamlit frontend runs separately and communicates with the FastAPI application.

## 5. Project Structure

```text
Distributed_Media_Processing_Microservice/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   └── job.py
│   ├── services/
│   │   ├── image_service.py
│   │   ├── redis_service.py
│   │   ├── s3_service.py
│   │   └── video_service.py
│   ├── __init__.py
│   ├── celery_app.py
│   ├── main.py
│   ├── metrics.py
│   └── tasks.py
├── frontend/
│   ├── app.py
│   └── requirements.txt
├── tests/
│   ├── test_image_service.py
│   ├── test_main.py
│   ├── test_redis_service.py
│   ├── test_s3_service.py
│   └── test_video_service.py
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 6. Implemented Components

### 6.1 FastAPI Application

FastAPI provides the REST API for job creation, file uploads, status tracking, and monitoring.

Implemented endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Returns the application message |
| POST | `/jobs` | Creates a media-processing job |
| GET | `/jobs/{job_id}` | Retrieves the current job status |
| POST | `/upload` | Uploads a media file to the shared local upload directory |
| POST | `/upload-url` | Generates a presigned Amazon S3 upload URL |
| GET | `/metrics` | Exposes Prometheus-compatible metrics |

Pydantic models validate job-creation and S3 upload-URL requests. FastAPI's `UploadFile` handles local media uploads.

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

The supported job-status values are:

```text
pending
processing
completed
failed
```

Clients can retrieve the current status using the job ID.

### 6.3 Celery Background Processing

Celery executes media-processing jobs asynchronously.

Instead of performing the media operation directly inside the API request, FastAPI submits a task to Celery. The worker then processes the job.

```text
FastAPI
   |
   v
Celery Task
   |
   v
RabbitMQ
   |
   v
Celery Worker
   |
   v
Media Processing
   |
   v
Redis Job Status
```

This separates API request handling from resource-intensive media processing.

### 6.4 RabbitMQ

RabbitMQ acts as the message broker for Celery.

It transports processing tasks between the application and the worker.

The Docker Compose configuration exposes:

- **AMQP:** Port `5672`
- **Management UI:** Port `15672`

The management interface can be accessed locally at:

`http://localhost:15672`

### 6.5 Redis Job Status and Worker Metrics

Redis stores job statuses using job-specific keys.

Example key:

```text
job:<job_id>
```

Example status:

```text
job:example-job-id -> completed
```

Redis also stores the latest worker CPU usage value, allowing the application to retrieve this metric through the monitoring endpoint.

### 6.6 Amazon S3 Integration

The S3 service uses Boto3 to generate presigned upload URLs.

The application supports two separate upload mechanisms:

**Local upload workflow**

- `POST /upload` accepts a media file.
- FastAPI saves the uploaded file to the shared local upload directory.
- The Celery worker accesses the uploaded file through the shared Docker volume.

**Amazon S3 upload workflow**

- `POST /upload-url` generates a presigned S3 upload URL.
- The response includes the upload URL and the S3 object name.
- The object name uses the `uploads/` prefix.

Example S3 object name:

```text
uploads/video.mp4
```

The S3 presigned URL workflow and the local upload workflow are separate mechanisms. Generating a presigned URL does not automatically upload a file to S3.

### 6.7 Pillow Image Processing

Pillow is used for image-processing operations.

The image-processing service includes:

- Image cropping
- Image resizing
- JPEG image compression

The image-processing logic is organized separately from the API and background-task logic.

### 6.8 FFmpeg Video Processing

FFmpeg is used for video-processing operations.

**Thumbnail extraction**

Extracts a video frame at a specified timestamp and saves it as an image.

**Video transcoding**

Converts video using H.264 video encoding and AAC audio encoding.

The Celery worker executes these operations as background tasks.

The supported video job operations are:

- `thumbnail`
- `transcode`

The worker saves generated files in the corresponding output directories.

## 7. Prometheus Metrics

A Prometheus-compatible `/metrics` endpoint is implemented for monitoring the application.

### 7.1 Queue Length

Metric name:

```text
queue_length
```

Tracks the number of messages waiting in the Celery queue.

### 7.2 Worker CPU Usage

Metric name:

```text
worker_cpu_usage
```

Tracks CPU usage as a percentage using `psutil`.

### 7.3 Accessing Metrics

Start the Docker services and open:

`http://localhost:8000/metrics`

Example metrics output:

```text
# HELP queue_length Number of jobs waiting in the queue
# TYPE queue_length gauge
queue_length 0.0

# HELP worker_cpu_usage CPU usage percentage of the worker
# TYPE worker_cpu_usage gauge
worker_cpu_usage 1.2
```

The displayed values are illustrative examples; actual metric values depend on the running environment.

## 8. Docker Deployment

The application uses Docker Compose to run the backend services.

### 8.1 Build and Start the Services

From the project root, run:

```powershell
docker compose up --build
```

This starts:

- FastAPI API
- Celery worker
- RabbitMQ
- Redis

### 8.2 Check Running Services

Open a separate PowerShell terminal in the project root and run:

```powershell
docker compose ps
```

The command displays the status of the configured containers.

### 8.3 Stop the Services

Run:

```powershell
docker compose down
```

This stops and removes the containers created by the Compose project. Named or external volumes, if configured, have their own lifecycle.

### 8.4 Shared Media Directories

The API and Celery worker use shared Docker bind mounts for local media files.

The directories are:

```text
uploads/
converted/
thumbnails/
```

These directories allow the worker to access uploaded files and save generated outputs where they can also be accessed from the host machine.

Generated media files are excluded from version control through `.gitignore`.

## 9. API Verification

The root endpoint was verified after starting the Docker environment.

**Request**

```http
GET http://localhost:8000/
```

**Response**

```json
{
  "message": "Distributed Media Processing Microservice"
}
```

**Observed result:** HTTP `200 OK`.

This confirmed that the FastAPI service was running and responding correctly during local verification.

## 10. Testing and Validation

Pytest is used for automated testing.

The test suite covers:

- Image processing
- FastAPI endpoints
- Redis services
- S3 services
- Video processing

The test suite was executed inside the Docker API container.

**Latest recorded result:**

```text
18 passed, 1 warning
```

The warning was related to a testing dependency deprecation and did not represent a test failure.

### Run the Tests

With the Docker services running, open a separate PowerShell terminal in the project root and execute:

```powershell
docker compose exec api pytest
```

The command runs the test suite inside the API container.

## 11. Load Testing

A basic API load test was performed against the root endpoint.

### Test Command

Run this in PowerShell while the API is running:

```powershell
1..50 | ForEach-Object {
    Invoke-WebRequest -UseBasicParsing http://localhost:8000/
}
```

### Result

The API successfully processed 50 sequential requests.

All observed responses returned:

```text
StatusCode : 200
```

with the expected application response.

### Load Test Conclusion

The root endpoint handled 50 sequential requests without HTTP failures during the local Docker test.

This was a basic functional load test, not a production-scale performance benchmark. It did not measure concurrent traffic, sustained throughput, latency percentiles, or maximum system capacity.

## 12. Memory Usage Analysis

Docker container memory usage was measured using:

```powershell
docker stats --no-stream
```

### Measured Baseline

| Service | Memory Usage |
|---|---:|
| Celery Worker | 44.89 MiB |
| FastAPI API | 69.14 MiB |
| RabbitMQ | 160.1 MiB |
| Redis | 9.09 MiB |

These measurements represent the observed baseline in the local development environment at the time of testing. Memory usage can vary depending on workload, container state, and system resources.

### Memory Analysis Conclusion

The baseline measurements did not indicate an immediate memory-consumption problem during the observed test.

The recorded values provide a reference point for future performance monitoring and optimization. Further measurements under representative workloads would be needed before drawing conclusions about production memory requirements.

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

The backend and supporting services run through Docker Compose. The optional Streamlit frontend runs as a separate Python application.

## 14. Current Project Status

### 14.1 Completed Backend Components

- FastAPI REST API
- Pydantic request models
- Amazon S3 presigned upload URL generation
- Local media upload endpoint
- Redis job-status storage
- Celery background processing
- RabbitMQ message broker
- Pillow image-processing service
- FFmpeg video-processing service
- Docker Compose environment
- Prometheus-compatible metrics endpoint
- Queue-length monitoring
- Worker CPU monitoring
- Automated test suite
- Docker-based test verification
- Basic API load testing
- Memory-usage measurement
- Deployment documentation

### 14.2 Completed Optional Enhancement

- Streamlit user interface
- Video file upload through the frontend
- Video transcoding job submission
- Thumbnail extraction job submission
- Job ID display
- Job-status refresh
- Shared local media directories between API and worker

### 14.3 Latest Recorded Validation

```text
API verification: Passed
Load test: 50 sequential requests returned HTTP 200
Automated tests: 18 passed, 1 warning
Metrics endpoint: Verified
Memory baseline: Measured
Video upload and processing: Verified
Thumbnail generation: Verified
Video transcoding: Verified
```

These results reflect the recorded local development tests, not a production deployment.

## 15. Repository

**GitHub Repository:**

https://github.com/Nasrin-Code/Distributed_Media_Processing_Microservice

The repository contains the application source code, automated tests, Docker configuration, dependency configuration, optional frontend, and project documentation.

## 16. Optional Enhancement: Streamlit Frontend

The Streamlit frontend is an additional enhancement beyond the original backend project requirements.

It provides a simple interface for interacting with the FastAPI media-processing service.

### 16.1 Features

- Upload video files through a Streamlit interface.
- Choose video transcoding or thumbnail extraction.
- Submit processing jobs to the FastAPI backend.
- Display the generated job ID.
- Refresh and view the current job status.
- Share uploaded files and generated outputs between the API and Celery worker through Docker bind mounts.

### 16.2 Technology Stack

- Streamlit
- Python Requests
- FastAPI
- Celery
- Redis
- RabbitMQ
- Docker Compose
- FFmpeg

### 16.3 Run the Optional Frontend

**Step 1: Start the backend**

Open a PowerShell terminal in the project root:

```powershell
docker compose up --build
```

Keep this terminal running.

**Step 2: Install frontend dependencies**

Open a second PowerShell terminal in the same project root. Activate your existing Python virtual environment if you use one, then run:

```powershell
pip install -r frontend/requirements.txt
```

**Step 3: Start Streamlit**

In the second terminal, run:

```powershell
streamlit run frontend/app.py
```

Streamlit will display the local URL for the frontend in the terminal. Open that URL in your browser.

The frontend connects to the backend at:

```text
http://localhost:8000
```

### 16.4 Upload and Process a Video

1. Open the Streamlit interface.
2. Select a video file in MP4, AVI, or MOV format.
3. Choose **Video Transcoding** or **Thumbnail Extraction**.
4. Select **Upload and Process**.
5. View the generated job ID and initial status.
6. Select **Refresh Job Status** to retrieve the latest status.

The API and Celery worker share the local upload and output directories through Docker bind mounts.

### 16.5 Validation

The optional frontend workflow was tested locally.

- Video uploads were processed successfully.
- Thumbnail extraction generated image files in the thumbnails directory.
- Video transcoding generated output files in the converted directory.
- Job status was retrieved through the backend API.
- The existing backend test suite continued to pass with 18 tests.

The frontend currently displays the job ID and status. Displaying or downloading generated output files directly from the interface would be a separate enhancement.

## 17. Conclusion

The Distributed Media Processing Microservice has progressed from a basic FastAPI backend into a distributed, containerized media-processing system.

The implementation combines:

- FastAPI for REST API services
- Celery for asynchronous processing
- RabbitMQ for task messaging
- Redis for job-status storage and worker metric storage
- Pillow for image processing
- FFmpeg for video processing
- Amazon S3 for presigned upload URL integration
- Prometheus-compatible metrics for monitoring
- Docker Compose for multi-service deployment
- Streamlit for an optional user-facing interface

The application was validated through automated testing, API verification, basic load testing, metrics verification, and memory-usage analysis. The optional frontend extends the backend with a user interface for video uploads, processing-job submission, and status tracking.

The project demonstrates practical implementation of REST APIs, asynchronous task processing, message brokering, media processing, monitoring, containerization, testing, and frontend-to-backend integration.
