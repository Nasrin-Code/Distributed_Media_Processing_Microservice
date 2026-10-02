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

def transcode_video(input_path: str, output_path: str) -> str:
    input_video = Path(input_path)
    output_video = Path(output_path)

    if not input_video.exists():
        raise FileNotFoundError(f"Video not found: {input_video}")
    output_video.parent.mkdir(parents=True, exist_ok=True)

    command = ["ffmpeg", "-y", "-i", str(input_video), "-c:v", "libx264", "-c:a", "aac", str(output_video)]

    subprocess.run(command, check=True, capture_output=True, text=True)

    return str(output_video)