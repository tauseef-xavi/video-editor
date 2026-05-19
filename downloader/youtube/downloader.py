import subprocess
import sys
from pathlib import Path

from downloader.base import Downloader


class YouTubeDownloader(Downloader):
    """Downloads a YouTube video to *output_path* using yt-dlp.

    Selects the best available MP4 stream and merges video + audio
    into a single MP4 container.
    """

    def download(self, url: str, output_path: Path) -> None:
        print(f"Downloading: {url}")
        result = subprocess.run(
            [
                sys.executable, "-m", "yt_dlp",
                "--format", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "--merge-output-format", "mp4",
                "--output", str(output_path),
                "--no-playlist",
                url,
            ]
        )
        if result.returncode != 0:
            raise RuntimeError(f"Download failed for: {url}")
        print(f"Downloaded to: {output_path}")
