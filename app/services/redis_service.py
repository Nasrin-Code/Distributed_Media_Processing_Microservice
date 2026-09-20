import redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

def set_job_status(job_id: str, status: str) -> None:
    redis_client.set(f"job:{job_id}", status)

def get_job_status(job_id: str) -> str | None:
    return redis_client.get(f"job:{job_id}")