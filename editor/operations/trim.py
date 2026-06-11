import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from editor.base.stream_operation import StreamOperation


def _parse_timestamp(ts: str) -> float:
    parts = [float(p) for p in reversed(ts.split(":"))]
    return sum(p * m for p, m in zip(parts, [1, 60, 3600]))


@dataclass
class TrimOperation(StreamOperation):
    """Extracts a time-bounded clip from a video using stream copy (no re-encode).

    Args:
        start: Start timestamp (HH:MM:SS, MM:SS, or plain seconds).
        end:   End timestamp   (HH:MM:SS, MM:SS, or plain seconds).
    """

    start: str
    end: str

    def apply(self, source: Path, output: Path) -> None:
        duration = _parse_timestamp(self.end) - _parse_timestamp(self.start)
        if duration <= 0:
            raise ValueError("End time must be after start time.")

        print(f"[trim] {self.start} → {self.end} ({duration:.1f}s): {source.name} → {output.name}")
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
            raise RuntimeError(f"Trim failed:\n{result.stderr}")
        print(f"[trim] Saved: {output}")

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "trim",
            "label": "Trim Clip",
            "params": [
                {
                    "name": "start",
                    "type": "timestamp",
                    "label": "Start time",
                    "default": "0:00",
                    "description": "HH:MM:SS, MM:SS, or seconds",
                },
                {
                    "name": "end",
                    "type": "timestamp",
                    "label": "End time",
                    "default": "0:10",
                    "description": "HH:MM:SS, MM:SS, or seconds",
                },
            ],
        }
