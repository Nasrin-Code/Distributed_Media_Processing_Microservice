import redis

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

def set_job_status(job_id: str, status: str) -> None:
    redis_client.set(f"job:{job_id}", status)

def get_job_status(job_id: str) -> str | None:
    return redis_client.get(f"job:{job_id}")

def set_worker_cpu_usage(cpu_usage: float) -> None:
    redis_client.set("worker_cpu_usage", cpu_usage)

def get_worker_cpu_usage() -> float:
    value = redis_client.get("worker_cpu_usage")
    return float(value) if value is not None else 0.0