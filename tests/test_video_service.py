import subprocess

import pytest

from app.services.video_service import extract_thumbnail


def test_extract_thumbnail_success(tmp_path, monkeypatch):
    video = tmp_path / "input.mp4"
    video.write_bytes(b"fake video")
    output = tmp_path / "thumbnails" / "thumbnail.jpg"

    def fake_run(command, **kwargs):
        return None

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = extract_thumbnail(str(video), str(output), 2)

    assert result == str(output)
    assert output.parent.exists()


def test_extract_thumbnail_missing_video(tmp_path):
    video = tmp_path / "missing.mp4"
    output = tmp_path / "thumbnail.jpg"

    with pytest.raises(FileNotFoundError):
        extract_thumbnail(str(video), str(output), 2)


def test_extract_thumbnail_ffmpeg_error(tmp_path, monkeypatch):
    video = tmp_path / "input.mp4"
    video.write_bytes(b"fake video")
    output = tmp_path / "thumbnail.jpg"

    def fake_run(command, **kwargs):
        raise subprocess.CalledProcessError(1, command)

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(subprocess.CalledProcessError):
        extract_thumbnail(str(video), str(output), 2)