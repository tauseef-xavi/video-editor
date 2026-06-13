from dataclasses import dataclass
from typing import Any

from editor.base.filter_operation import FilterOperation
from editor.graph.filter_graph import FilterGraph
from editor.operations.effects.base import SimpleVideoEffect


@dataclass
class BlurOperation(FilterOperation):
    """Applies a Gaussian blur.

    Args:
        sigma: Blur radius. Higher values produce more blur. Default: 5.
    """

    sigma: int = 5

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        out = graph.next_pad("v")
        graph.add_node(f"{video_in}gblur=sigma={self.sigma}{out}")
        return out, audio_in

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "blur",
            "label": "Blur",
            "params": [
                {"name": "sigma", "type": "int", "label": "Radius", "default": 5, "min": 1, "max": 50},
            ],
        }


@dataclass
class EdgeDetectOperation(FilterOperation):
    """Traces edges in the video, producing a sketch-like outline effect.

    Args:
        low:  Low threshold for edge detection (0.0–1.0). Default: 0.1.
        high: High threshold for edge detection (0.0–1.0). Default: 0.4.
    """

    low: float = 0.1
    high: float = 0.4

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        out = graph.next_pad("v")
        graph.add_node(f"{video_in}edgedetect=low={self.low}:high={self.high}{out}")
        return out, audio_in

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "edge_detect",
            "label": "Edge Detect",
            "params": [
                {"name": "low", "type": "float", "label": "Low threshold", "default": 0.1, "min": 0.0, "max": 1.0},
                {"name": "high", "type": "float", "label": "High threshold", "default": 0.4, "min": 0.0, "max": 1.0},
            ],
        }


@dataclass
class PosterizeOperation(FilterOperation):
    """Reduces the colour palette to a fixed number of colours for a flat, graphic look.

    Uses ffmpeg's elbg filter (ELBG algorithm), the modern posterize equivalent.

    Args:
        colors: Number of colours in the output palette (2–256). Lower values
                produce a more extreme effect. Default: 16.
    """

    colors: int = 16

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        out = graph.next_pad("v")
        graph.add_node(f"{video_in}elbg=codebook_length={self.colors}{out}")
        return out, audio_in

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "posterize",
            "label": "Posterize",
            "params": [
                {"name": "colors", "type": "int", "label": "Colors", "default": 16, "min": 2, "max": 256},
            ],
        }


@dataclass
class PixelizeOperation(FilterOperation):
    """Pixelates the video into a mosaic of large blocks.

    Args:
        width:  Block width in pixels. Default: 16.
        height: Block height in pixels. Default: 16.
    """

    width: int = 16
    height: int = 16

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        out = graph.next_pad("v")
        graph.add_node(f"{video_in}pixelize=width={self.width}:height={self.height}{out}")
        return out, audio_in

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "pixelize",
            "label": "Pixelize",
            "params": [
                {"name": "width", "type": "int", "label": "Block width", "default": 16, "min": 2, "max": 256},
                {"name": "height", "type": "int", "label": "Block height", "default": 16, "min": 2, "max": 256},
            ],
        }


@dataclass
class SharpenOperation(SimpleVideoEffect):
    """Sharpens edges using an unsharp mask with sensible defaults."""

    @classmethod
    def filter_string(cls) -> str:
        return "unsharp=5:5:1.0:5:5:0.0"

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {"name": "sharpen", "label": "Sharpen", "params": []}


@dataclass
class VignetteOperation(FilterOperation):
    """Darkens the corners to draw focus towards the centre.

    Args:
        angle: Falloff radius in radians. Range 0.0–PI/2 (~1.57).
               Higher values produce a stronger, tighter vignette.
               Default: 1.0 (moderate).
    """

    angle: float = 1.0

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        out = graph.next_pad("v")
        graph.add_node(f"{video_in}vignette=angle={self.angle}{out}")
        return out, audio_in

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "vignette",
            "label": "Vignette",
            "params": [
                {"name": "angle", "type": "float", "label": "Strength", "default": 1.0, "min": 0.0, "max": 1.5708},
            ],
        }
