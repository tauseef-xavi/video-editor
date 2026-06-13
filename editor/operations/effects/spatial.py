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
