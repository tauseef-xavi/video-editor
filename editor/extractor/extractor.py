import subprocess
import sys
from pathlib import Path

from editor.base import Editor


def _parse_timestamp(ts: str) -> float:
    parts = [float(p) for p in reversed(ts.split(":"))]
    return sum(p * m for p, m in zip(parts, [1, 60, 3600]))


def check_ffmpeg() -> None:
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    if result.returncode != 0:
        print("Error: ffmpeg not found. Install it with: brew install ffmpeg")
        sys.exit(1)


class ClipExtractor(Editor):
    """Extracts a time-bounded clip from a video file using ffmpeg.

    Args:
        start: Start timestamp (HH:MM:SS, MM:SS, or plain seconds).
        end:   End timestamp   (HH:MM:SS, MM:SS, or plain seconds).
    """

    def __init__(self, start: str, end: str) -> None:
        self.start = start
        self.end = end

    def edit(self, source: Path, output: Path) -> None:
        duration = _parse_timestamp(self.end) - _parse_timestamp(self.start)
        if duration <= 0:
            raise ValueError("End time must be after start time.")

        print(f"Extracting {self.start} → {self.end} ({duration:.1f}s) into {output}")
        result = subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(source),
                "-ss", self.start,
                "-t", str(duration),
                "-c", "copy",
                str(output),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg extraction failed:\n{result.stderr}")
        print(f"Clip saved: {output}")
