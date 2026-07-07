import os
import subprocess
from typing import Protocol


class FfmpegAdapter(Protocol):
    def extract_audio(self, video_path: str, output_dir: str) -> str: ...

    def generate_thumbnail(self, video_path: str, output_dir: str) -> str: ...


class FakeFfmpegAdapter:
    def extract_audio(self, video_path: str, output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "audio.mp3")
        with open(path, "wb") as f:
            f.write(b"fake audio content")
        return path

    def generate_thumbnail(self, video_path: str, output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "thumbnail.jpg")
        with open(path, "wb") as f:
            f.write(b"fake thumbnail content")
        return path


class RealFfmpegAdapter:
    def extract_audio(self, video_path: str, output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(output_dir, f"{base}.mp3")
        subprocess.run(
            [
                "ffmpeg", "-i", video_path,
                "-vn", "-acodec", "libmp3lame",
                "-y", output_path,
            ],
            check=True,
            capture_output=True,
        )
        return output_path

    def generate_thumbnail(self, video_path: str, output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(output_dir, f"{base}.jpg")
        subprocess.run(
            [
                "ffmpeg", "-i", video_path,
                "-ss", "00:00:01",
                "-vframes", "1",
                "-y", output_path,
            ],
            check=True,
            capture_output=True,
        )
        return output_path
