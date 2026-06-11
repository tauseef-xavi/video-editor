from dataclasses import dataclass
from typing import Any

from editor.base.filter_operation import FilterOperation
from editor.graph.filter_graph import FilterGraph
from editor.operations.effects.base import SimpleVideoEffect


@dataclass
class GrayscaleOperation(SimpleVideoEffect):
    """Converts the video to black and white."""

    @classmethod
    def filter_string(cls) -> str:
        return "hue=s=0"

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {"name": "grayscale", "label": "Grayscale", "params": []}


@dataclass
class SepiaOperation(SimpleVideoEffect):
    """Applies a warm sepia tone."""

    @classmethod
    def filter_string(cls) -> str:
        return "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131"

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {"name": "sepia", "label": "Sepia", "params": []}


@dataclass
class BrightnessOperation(FilterOperation):
    """Adjusts brightness and contrast independently.

    Args:
        brightness: Offset in range -1.0 to 1.0. Default: 0.0 (no change).
        contrast:   Multiplier >= 0. Default: 1.0 (no change).
    """

    brightness: float = 0.0
    contrast: float = 1.0

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        out = graph.next_pad("v")
        graph.add_node(f"{video_in}eq=brightness={self.brightness}:contrast={self.contrast}{out}")
        return out, audio_in

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "brightness",
            "label": "Brightness & Contrast",
            "params": [
                {"name": "brightness", "type": "float", "label": "Brightness", "default": 0.0, "min": -1.0, "max": 1.0},
                {"name": "contrast", "type": "float", "label": "Contrast", "default": 1.0, "min": 0.0, "max": 3.0},
            ],
        }


@dataclass
class SaturationOperation(FilterOperation):
    """Adjusts colour saturation.

    Args:
        level: Saturation multiplier. ``0.0`` = grayscale, ``1.0`` = original,
               ``2.0`` = double saturation.
    """

    level: float = 1.0

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        out = graph.next_pad("v")
        graph.add_node(f"{video_in}hue=s={self.level}{out}")
        return out, audio_in

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "saturation",
            "label": "Saturation",
            "params": [
                {"name": "level", "type": "float", "label": "Level", "default": 1.0, "min": 0.0, "max": 3.0},
            ],
        }
