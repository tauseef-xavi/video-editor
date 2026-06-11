# multimedia

A Python toolkit for downloading YouTube clips, applying video/audio editing operations, and re-encoding output for social platforms or file-size targets.

## Requirements

- Python 3.12+
- [ffmpeg](https://ffmpeg.org/) — `brew install ffmpeg`
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — `pip install yt-dlp`

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install yt-dlp
```

## Architecture

The codebase is split into three top-level modules.

### `downloader`

Downloads a YouTube video to a local file using `yt-dlp`. Selects the best available MP4 stream and merges video and audio into a single container.

```
downloader/
├── base/       # Abstract Downloader
└── youtube/    # YouTubeDownloader
```

### `editor`

Applies editing and visual effect operations to a video file. The pipeline executes in two tiers so that structural edits (trim) stay lossless and all filter operations compose into a single ffmpeg re-encode pass.

```
editor/
├── base/
│   ├── operation.py          # EditOperation — root abstract base + schema() contract
│   ├── stream_operation.py   # StreamOperation — stream copy, no re-encode
│   └── filter_operation.py   # FilterOperation — contributes to -filter_complex graph
├── graph/
│   ├── filter_graph.py       # Accumulates filter nodes and extra inputs
│   └── runner.py             # FFmpegRunner — the only ffmpeg subprocess site
├── operations/
│   ├── trim.py               # TrimOperation (StreamOperation)
│   ├── flip.py               # FlipOperation
│   ├── volume.py             # VolumeOperation
│   ├── text_overlay.py       # TextOverlayOperation
│   ├── pip.py                # PictureInPictureOperation
│   └── effects/
│       ├── base.py           # SimpleVideoEffect — for single-string filter effects
│       ├── color.py          # Grayscale, Sepia, Brightness, Saturation
│       ├── spatial.py        # Blur, Sharpen, Vignette
│       └── temporal.py       # Speed, FadeIn, FadeOut
├── pipeline/   # EditorPipeline — orchestrates two-tier execution
├── registry/   # REGISTRY dict + schemas() for UI consumers
└── utils/      # check_ffmpeg
```

**Two-tier execution**

```
source.mp4
    │
    ▼  Stream tier  — ffmpeg -c copy  (TrimOperation, lossless)
trimmed.mp4
    │
    ▼  Filter tier  — ffmpeg -filter_complex "..."  (all FilterOperations, one pass)
output.mp4
```

N chained filter operations always produce exactly one re-encode.

**Available operations**

| Name | Type | Key parameters |
|---|---|---|
| `TrimOperation` | StreamOperation | `start`, `end` |
| `FlipOperation` | FilterOperation | `direction` (`horizontal`/`vertical`) |
| `VolumeOperation` | FilterOperation | `level` (multiplier) |
| `TextOverlayOperation` | FilterOperation | `text`, `x`, `y`, `font_size`, `color` |
| `PictureInPictureOperation` | FilterOperation | `overlay_path`, `x`, `y`, `scale` |
| `GrayscaleOperation` | SimpleVideoEffect | — |
| `SepiaOperation` | SimpleVideoEffect | — |
| `BrightnessOperation` | FilterOperation | `brightness`, `contrast` |
| `SaturationOperation` | FilterOperation | `level` |
| `BlurOperation` | FilterOperation | `sigma` |
| `SharpenOperation` | SimpleVideoEffect | — |
| `VignetteOperation` | SimpleVideoEffect | — |
| `SpeedOperation` | FilterOperation | `factor` (0.5–2.0) |
| `FadeInOperation` | FilterOperation | `duration` |
| `FadeOutOperation` | FilterOperation | `start`, `duration` |

**Programmatic use**

```python
from editor import EditorPipeline, TrimOperation, GrayscaleOperation, TextOverlayOperation, FadeInOperation

pipeline = EditorPipeline([
    TrimOperation("0:30", "1:00"),
    GrayscaleOperation(),
    TextOverlayOperation(text="Hello", color="white"),
    FadeInOperation(duration=1.0),
])
pipeline.run(Path("source.mp4"), Path("result.mp4"))
```

**Adding a new effect**

For a parameterless effect, subclass `SimpleVideoEffect` and return the ffmpeg filter string:

```python
from dataclasses import dataclass
from editor.operations.effects.base import SimpleVideoEffect

@dataclass
class NegativeOperation(SimpleVideoEffect):
    @classmethod
    def filter_string(cls) -> str:
        return "negate"

    @classmethod
    def schema(cls) -> dict:
        return {"name": "negative", "label": "Negative", "params": []}
```

For a parametric effect, subclass `FilterOperation` and implement `add_to_graph()`.

Register it in `editor/registry/registry.py` to make it available to the CLI and any UI consumer.

---

### `codec`

Re-encodes a video with quality-reduction or platform-specific settings. Uses the Strategy pattern — individual strategies are composable via `OptimizationPipeline`.

```
codec/
├── pipeline/          # OptimizationPipeline — chains strategies sequentially
└── strategies/
    ├── base/          # Abstract CodecStrategy
    ├── optimization/  # CRFReductionStrategy, ScaleReductionStrategy, BitrateCapStrategy
    └── social/        # TwitterCodec (H.264/AAC/yuv420p/faststart)
```

**Codec strategies**

| Strategy | Effect | Defaults |
|---|---|---|
| `CRFReductionStrategy` | Raises CRF for a smaller file | CRF 28, preset `slow` |
| `ScaleReductionStrategy` | Downscales resolution (aspect ratio preserved) | 480p |
| `BitrateCapStrategy` | Hard-caps video and audio bitrate | video `1000k`, audio `96k` |
| `TwitterCodec` | H.264/AAC, yuv420p, faststart | — |
