import subprocess
from pathlib import Path

def extract_thumbnail(video_path: str, output_path: str, timestamp: int = 2) -> str:
    video = Path(video_path)
    output = Path(output_path)

    if not video.exists():
        raise FileNotFoundError(f"Video not found: {video}")
    output.parent.mkdir(parents=True, exist_ok=True)

    command = ["ffmpeg", "-y", "-i", str(video), "-ss", str(timestamp), "-frames:v", "1", "-update", "1", str(output)]

    subprocess.run(command, check=True, capture_output=True, text=True)

    return str(output)