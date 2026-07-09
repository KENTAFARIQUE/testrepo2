import os
from typing import Protocol


class Downloader(Protocol):
    def download(self, url: str, work_dir: str) -> str: ...


class FakeDownloader:
    def download(self, url: str, work_dir: str) -> str:
        os.makedirs(work_dir, exist_ok=True)
        path = os.path.join(work_dir, "fake_video.mp4")
        with open(path, "wb") as f:
            f.write(b"fake video content")
        return path


class RealYoutubeDownloader:
    def download(self, url: str, work_dir: str) -> str:
        import subprocess
        import logging

        os.makedirs(work_dir, exist_ok=True)
        tmpl = os.path.join(work_dir, "%(id)s.%(ext)s")
        logging.info("ytdl subprocess: work_dir=%s tmpl=%s url=%s", work_dir, tmpl, url)
        result = subprocess.run(
            [
                "yt-dlp",
                "--format", "b",
                "--output", tmpl,
                "--print", "after_move:%(id)s.%(ext)s",
                "--force-ipv4",
                "--no-playlist",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=300,
        )
        logging.info("ytdl subprocess: rc=%d stdout=%r stderr=%r", result.returncode, result.stdout[:200], result.stderr[:200])
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip())
        filename = result.stdout.strip().split("\n")[-1]
        full_path = os.path.join(work_dir, filename)
        logging.info("ytdl subprocess: success path=%s", full_path)
        return full_path
