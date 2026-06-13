#!/usr/bin/env python3
import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from downloader.youtube import YouTubeDownloader
from editor import (
    EditorPipeline,
    PixelizeOperation,
    PosterizeOperation,
    TrimOperation,
    check_ffmpeg,
)

URL = os.environ["VIDEO_URL"]
START = "0:10"
END = "0:40"

# Each entry: (output filename, filter operations applied after trim)
VARIANTS = [
    # ("output_sepia_vignette.mp4", [
    #     SepiaOperation(),
    #     VignetteOperation(angle=1.5),
    #     FadeInOperation(duration=1.5),
    # ]),
    # ("output_edge_detect.mp4", [
    #     GrayscaleOperation(),
    #     EdgeDetectOperation(low=0.1, high=0.4),
    # ]),
    ("output_posterize.mp4", [
        PosterizeOperation(colors=16),
    ]),
    ("output_pixelize.mp4", [
        PixelizeOperation(width=16, height=16),
    ]),
]


def main():
    check_ffmpeg()

    with tempfile.TemporaryDirectory() as tmpdir:
        source = Path(tmpdir) / "source.mp4"
        YouTubeDownloader().download(URL, source)

        trimmed = Path(tmpdir) / "trimmed.mp4"
        EditorPipeline([TrimOperation(START, END)]).run(source, trimmed)

        for filename, filter_ops in VARIANTS:
            print(f"\n--- {filename} ---")
            EditorPipeline(filter_ops).run(trimmed, Path(filename))

    print("\nAll outputs ready:")
    for filename, _ in VARIANTS:
        print(f"  {filename}")


if __name__ == "__main__":
    main()
