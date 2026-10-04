from pathlib import Path

from app.celery_app import celery_app
from app.services.redis_service import set_job_status
from app.services.video_service import transcode_video, extract_thumbnail


@celery_app.task(bind=True)
def process_job(self, job_id: str, filename: str, operation: str):
    try:
        print(f"Received job: {job_id}")
        print(f"Processing {filename} with operation: {operation}")

        set_job_status(job_id, "processing")

        input_path = Path("sample_videos") / filename

        if operation == "transcode":
            output_path = Path("converted") / f"{Path(filename).stem}_converted.mp4"

            transcode_video(
                str(input_path),
                str(output_path),
            )

            print(f"Transcoding completed: {output_path}")

        elif operation == "thumbnail":
            output_path = Path("thumbnails") / f"{Path(filename).stem}_thumbnail.jpg"

            extract_thumbnail(
                str(input_path),
                str(output_path),
            )

            print(f"Thumbnail extraction completed: {output_path}")

        else:
            raise ValueError(f"Unsupported operation: {operation}")

        set_job_status(job_id, "completed")

        return {
            "job_id": job_id,
            "filename": filename,
            "operation": operation,
            "status": "completed",
        }

    except TimeoutError as error:
        print(f"Network timeout for job {job_id}: {error}")
        raise self.retry(exc=error, countdown=5)

    except Exception as error:
        print(f"Job {job_id} failed: {error}")
        set_job_status(job_id, "failed")
        raise