import subprocess
import sys


def check_ffmpeg() -> None:
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    if result.returncode != 0:
        print("Error: ffmpeg not found. Install it with: brew install ffmpeg")
        sys.exit(1)
