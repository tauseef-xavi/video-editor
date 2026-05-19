import subprocess
from pathlib import Path

from codec.strategies.base import CodecStrategy


class TwitterCodec(CodecStrategy):
    """H.264/AAC, yuv420p, faststart — required for Twitter uploads."""

    def convert(self, source: Path, output: Path) -> None:
        print(f"[twitter] Converting {source.name} → {output.name}")
        result = subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(source),
                "-vcodec", "libx264",
                "-acodec", "aac",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                str(output),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Twitter conversion failed:\n{result.stderr}")
        print(f"[twitter] Saved: {output}")
