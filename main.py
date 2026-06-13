#!/usr/bin/env python3
import tempfile
from pathlib import Path

from downloader.youtube import YouTubeDownloader
from editor import (
    EditorPipeline,
    FadeInOperation,
    GrayscaleOperation,
    SepiaOperation,
    TrimOperation,
    VignetteOperation,
    check_ffmpeg,
)

URL = "https://www.youtube.com/watch?v=<VIDEO_ID>"
OUTPUT = Path("output.mp4")


def main():
    check_ffmpeg()

    with tempfile.TemporaryDirectory() as tmpdir:
        source = Path(tmpdir) / "source.mp4"
        YouTubeDownloader().download(URL, source)

        EditorPipeline([
            TrimOperation(start="0:10", end="0:40"),
            GrayscaleOperation(),
            SepiaOperation(),
            FadeInOperation(duration=1.5),
            VignetteOperation(angle=1.5),
        ]).run(source, OUTPUT)

    print(f"Done → {OUTPUT}")


if __name__ == "__main__":
    main()
