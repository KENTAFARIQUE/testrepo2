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
        import yt_dlp

        os.makedirs(work_dir, exist_ok=True)
        ydl_opts = {
            "outtmpl": os.path.join(work_dir, "%(id)s.%(ext)s"),
            "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "quiet": True,
            "force_ipv4": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore[arg-type]
            info = ydl.extract_info(url, download=True)
            return os.path.join(work_dir, f"{info['id']}.{info['ext']}")  # type: ignore[index]
