import subprocess
from pathlib import Path

from codec.strategies.base import CodecStrategy


class ScaleReductionStrategy(CodecStrategy):
    """Reduces file size by downscaling video resolution.

    The width is calculated automatically to preserve the original aspect ratio
    (FFmpeg ``scale=-2:<height>`` ensures width stays divisible by 2).

    Args:
        height: Target video height in pixels. Default: 480 (480p).
    """

    def __init__(self, height: int = 480) -> None:
        self.height = height

    def convert(self, source: Path, output: Path) -> None:
        print(f"[scale] Downscaling to {self.height}p: {source.name} → {output.name}")
        result = subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(source),
                "-vf", f"scale=-2:{self.height}",
                "-c:a", "copy",
                str(output),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Scale reduction failed:\n{result.stderr}")
        print(f"[scale] Saved: {output}")
