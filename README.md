# Distributed Media Processing Microservice

## 2nd Month Internship Project — Mid-Review Report

**Organization:** Zaalima Development Pvt. Ltd.
**Project:** Distributed Media Processing Microservice
**Developer:** Nasrin A
**Programming Language:** Python
**Framework:** FastAPI
**Current Progress:** Day 17 — Pillow Image Processing

---

## 1. Project Overview

The Distributed Media Processing Microservice is a Python-based backend project designed to provide APIs and supporting services for media processing workflows.

The project uses FastAPI to expose API endpoints, Amazon S3 integration for upload handling, Redis for job-status storage, and Celery as the planned background task-processing component. Pillow is used to implement image-processing operations.

The project is being developed incrementally, with an emphasis on modular code organization, automated testing, and integration of backend services.

## 2. Project Objectives

* Develop REST API endpoints using FastAPI.
* Implement media-processing operations using Python.
* Integrate Amazon S3 presigned URLs for file uploads.
* Use Redis to store and retrieve processing job statuses.
* Prepare background processing with Celery.
* Organize the application into reusable service modules.
* Write automated tests to verify application functionality.
* Build toward a distributed media-processing workflow.

## 3. Technology Stack

| Technology        | Purpose                                   |
| ----------------- | ----------------------------------------- |
| Python            | Core programming language                 |
| FastAPI           | Backend API framework                     |
| Uvicorn           | ASGI application server                   |
| Pydantic          | Request and data validation               |
| Pillow            | Image cropping, resizing, and compression |
| Amazon S3 / Boto3 | Object storage and upload URL integration |
| Redis             | Job-status storage                        |
| Celery            | Background task processing                |
| Pytest            | Automated testing                         |
| HTTPX             | HTTP testing support                      |
| Docker            | Running supporting services locally       |
| Git and GitHub    | Version control and source-code hosting   |

## 4. Project Structure

```text
Distributed_Media_Processing_Microservice/
│
├── app/
│   ├── services/
│   │   ├── image_service.py
│   │   ├── redis_service.py
│   │   └── s3_service.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_image_service.py
│   ├── test_main.py
│   ├── test_redis_service.py
│   └── test_s3_service.py
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

*The structure above represents the known project files; retain any additional files and folders already present in the repository.*

## 5. Implemented Components

### 5.1 FastAPI Application

FastAPI is used to build the backend API.

Implemented endpoints include:

* `GET /` — returns an application message.
* `POST /jobs` — accepts a job request and returns job information.
* `POST /upload-url` — accepts an upload request and generates a presigned upload URL through the S3 service.

Pydantic request models are used for structured request data and validation.

### 5.2 Amazon S3 Integration

The S3 service supports generating presigned upload URLs.

The upload URL endpoint uses the requested filename to construct an object name under the `uploads/` prefix.

Example object name:

```text
uploads/video.mp4
```

This provides a way for clients to upload media to object storage without sending the file through the API server itself.

### 5.3 Redis Job Status

Redis is used to store and retrieve job statuses.

The project has tested status values such as:

* `pending`
* `processing`
* `completed`
* `failed`

The Redis service has been tested locally using a Redis Docker container and the Python Redis client.

### 5.4 Pillow Image Processing

Pillow is used for the image-processing service. The following operations have been implemented:

**Image cropping**

The `crop_image()` function accepts an image and crop coordinates and returns the selected region.

**Image resizing**

The `resize_image()` function accepts an image, target width, and target height. It uses Pillow's LANCZOS resampling filter.

**Image compression**

The `compress_image()` function converts the image to RGB and encodes it as JPEG using a configurable quality value and optimization.

The JPEG data is written to an in-memory `BytesIO` buffer, then reopened as a Pillow image.

## 6. Development Progress

### Week 1 and Week 2

The project has been developed incrementally, establishing its backend application, API structure, supporting services, and testing foundation.

The current repository includes FastAPI endpoints, S3 integration, Redis status functionality, and automated tests.

### Week 3 — Core Media Processing Logic

**Day 15 — Image Cropping**

* Installed Pillow.
* Created the image-processing service.
* Implemented image cropping.
* Added an automated crop test.

**Day 16 — Image Resizing**

* Implemented image resizing using Pillow.
* Used the LANCZOS resampling filter.
* Added an automated resize test.

**Day 17 — Image Compression**

* Implemented JPEG image compression.
* Used `BytesIO` for in-memory image data.
* Added an automated compression test.
* Verified the full test suite.

## 7. Testing and Validation

Pytest is used to run the automated test suite.

The latest recorded test run collected 12 tests across the image-processing, API, Redis, and S3 test modules.

**Latest result: 12 passed, 1 warning.**

| Test module             | Tests passed |
| ----------------------- | -----------: |
| `test_image_service.py` |            3 |
| `test_main.py`          |            4 |
| `test_redis_service.py` |            2 |
| `test_s3_service.py`    |            3 |
| **Total**               |       **12** |

The warning is a deprecation warning associated with the Starlette/AnyIO testing dependency.

## 8. Local Development Environment

The project is developed using:

* Windows
* Visual Studio Code
* Python virtual environment (`.venv`)
* PowerShell
* Docker for local supporting services

The required Python packages are listed in `requirements.txt`.

## 9. Current Project Status

**Completed and tested**

* FastAPI application and implemented API endpoints.
* S3 presigned upload URL functionality.
* Redis job-status service.
* Pillow image cropping.
* Pillow image resizing.
* Pillow JPEG compression.
* Automated tests for the implemented components.

**Planned / upcoming**

* FFmpeg-based media processing, including thumbnail generation and transcoding.
* Integration of processing scripts with Celery workers.
* End-to-end testing of the complete processing workflow.
* Further validation and project submission documentation.

The complete distributed processing workflow is still under development.

## 10. Repository

**GitHub:**
https://github.com/Nasrin-Code/Distributed_Media_Processing_Microservice

The repository contains the project's source code, tests, configuration, dependency list, and documentation.

## 11. Conclusion

The project has established a backend foundation for a distributed media-processing system. It includes API endpoints, storage integration, Redis-based job-status handling, and tested image-processing functions using Pillow.

The next development phase will focus on FFmpeg processing and background worker integration, progressing toward an end-to-end media-processing workflow.
