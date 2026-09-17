import boto3

S3_BUCKET_NAME ="distributed-media-processing-nasrin"

s3_client = boto3.client("s3")

def upload_file(file_path: str, object_name: str) -> None:
    s3_client.upload_file(file_path, S3_BUCKET_NAME, object_name)

def download_file(object_name: str, destination_path: str) -> None:
    s3_client.download_file(S3_BUCKET_NAME, object_name, destination_path)