import subprocess
from pathlib import Path

from codec.strategies.base import CodecStrategy


class CRFReductionStrategy(CodecStrategy):
    """Reduces file size by increasing CRF (higher value = lower quality, smaller file).

    Args:
        crf:    Constant Rate Factor for libx264. Range 18–51; default 28.
                18 ≈ near-lossless, 51 = worst quality.
        preset: FFmpeg encoding preset (ultrafast…veryslow). Slower presets
                compress better at the same CRF. Default: "slow".
    """

    def __init__(self, crf: int = 28, preset: str = "slow") -> None:
        self.crf = crf
        self.preset = preset

    def convert(self, source: Path, output: Path) -> None:
        print(f"[crf] CRF={self.crf}, preset={self.preset}: {source.name} → {output.name}")
        result = subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(source),
                "-vcodec", "libx264",
                "-crf", str(self.crf),
                "-preset", self.preset,
                "-acodec", "aac",
                str(output),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"CRF reduction failed:\n{result.stderr}")
        print(f"[crf] Saved: {output}")
