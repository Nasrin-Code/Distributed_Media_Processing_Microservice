from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Distributed Media Processing Microservice"
    }


def test_create_job():
    response = client.post(
        "/jobs",
        json={
            "filename": "video.mp4",
            "operation": "resize",
        },
    )

    assert response.status_code == 200
    data = response.json()
    
    assert data["filename"] == "video.mp4"
    assert data["operation"] == "resize"
    assert data["status"] == "pending"
    assert "job_id" in data

def test_get_missing_job():
    response = client.get("/jobs/job-that-does-not-exist")

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}

@patch("app.main.generate_upload_url")
def test_create_upload_url(mock_generate_upload_url):
    mock_generate_upload_url.return_value = "https://example.com/upload"

    response = client.post(
        "/upload-url",
        json={"filename": "video.mp4"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "upload_url": "https://example.com/upload",
        "object_name": "uploads/video.mp4",
    }

    mock_generate_upload_url.assert_called_once_with(
        "uploads/video.mp4"
    )