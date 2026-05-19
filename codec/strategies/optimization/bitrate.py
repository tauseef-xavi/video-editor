import subprocess
from pathlib import Path

from codec.strategies.base import CodecStrategy


class BitrateCapStrategy(CodecStrategy):
    """Reduces file size by hard-capping video and audio bitrate.

    Uses ``-b:v`` / ``-maxrate`` / ``-bufsize`` for video and ``-b:a`` for
    audio. The buffer size is set to 2× the video bitrate, which is a
    standard heuristic for smooth VBR playback within the cap.

    Args:
        video_bitrate: Target video bitrate, e.g. ``"1000k"`` or ``"2M"``.
                       Default: ``"1000k"``.
        audio_bitrate: Target audio bitrate, e.g. ``"96k"``. Default: ``"96k"``.
    """

    def __init__(self, video_bitrate: str = "1000k", audio_bitrate: str = "96k") -> None:
        self.video_bitrate = video_bitrate
        self.audio_bitrate = audio_bitrate

    def _bufsize(self) -> str:
        """Return 2× video_bitrate as a kbps string for -bufsize."""
        raw = self.video_bitrate.lower()
        if raw.endswith("m"):
            kb = int(float(raw[:-1]) * 1024)
        elif raw.endswith("k"):
            kb = int(raw[:-1])
        else:
            kb = int(raw) // 1000
        return f"{kb * 2}k"

    def convert(self, source: Path, output: Path) -> None:
        print(
            f"[bitrate] Cap v:{self.video_bitrate} a:{self.audio_bitrate}: "
            f"{source.name} → {output.name}"
        )
        result = subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(source),
                "-b:v", self.video_bitrate,
                "-maxrate", self.video_bitrate,
                "-bufsize", self._bufsize(),
                "-b:a", self.audio_bitrate,
                str(output),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Bitrate cap failed:\n{result.stderr}")
        print(f"[bitrate] Saved: {output}")
