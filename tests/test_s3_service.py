from unittest.mock import patch

from app.services.s3_service import (
    S3_BUCKET_NAME,
    download_file,
    upload_file,
    generate_upload_url
)


@patch("app.services.s3_service.s3_client")
def test_upload_file(mock_s3_client):
    upload_file("photo.jpg", "uploads/photo.jpg")

    mock_s3_client.upload_file.assert_called_once_with(
        "photo.jpg",
        S3_BUCKET_NAME,
        "uploads/photo.jpg",
    )


@patch("app.services.s3_service.s3_client")
def test_download_file(mock_s3_client):
    download_file("uploads/photo.jpg", "downloaded-photo.jpg")

    mock_s3_client.download_file.assert_called_once_with(
        S3_BUCKET_NAME,
        "uploads/photo.jpg",
        "downloaded-photo.jpg",
    )

@patch("app.services.s3_service.s3_client")
def test_generate_upload_url(mock_s3_client):
    mock_s3_client.generate_presigned_url.return_value = (
        "https://example.com/presigned-url"
    )

    result = generate_upload_url(
        "uploads/video.mp4",
        expiration=3600,
    )

    assert result == "https://example.com/presigned-url"

    mock_s3_client.generate_presigned_url.assert_called_once_with(
        "put_object",
        Params={
            "Bucket": S3_BUCKET_NAME,
            "Key": "uploads/video.mp4",
        },
        ExpiresIn=3600,
    )