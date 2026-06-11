from dataclasses import dataclass
from pathlib import Path
from typing import Any

from editor.base.filter_operation import FilterOperation
from editor.graph.filter_graph import FilterGraph


@dataclass
class PictureInPictureOperation(FilterOperation):
    """Overlays a secondary video in a corner of the main video.

    The overlay is scaled to a fraction of the main video width before
    compositing so it stays proportional regardless of source resolution.

    Args:
        overlay_path: Path to the secondary video file.
        x:            Horizontal offset of the overlay in pixels. Default: 10.
        y:            Vertical offset of the overlay in pixels. Default: 10.
        scale:        Overlay width as a fraction of the main video width.
                      Default: ``0.25`` (quarter-width).
    """

    overlay_path: Path
    x: int = 10
    y: int = 10
    scale: float = 0.25

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        idx = graph.add_input(self.overlay_path)
        scaled = graph.next_pad("pip")
        out = graph.next_pad("v")
        graph.add_node(f"[{idx}:v]scale=iw*{self.scale}:-1{scaled}")
        graph.add_node(f"{video_in}{scaled}overlay={self.x}:{self.y}{out}")
        return out, audio_in  # overlay audio is ignored; main audio passes through

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "pip",
            "label": "Picture-in-Picture",
            "params": [
                {"name": "overlay_path", "type": "file", "label": "Overlay video", "default": ""},
                {"name": "x", "type": "int", "label": "X offset", "default": 10, "min": 0},
                {"name": "y", "type": "int", "label": "Y offset", "default": 10, "min": 0},
                {
                    "name": "scale",
                    "type": "float",
                    "label": "Overlay scale",
                    "default": 0.25,
                    "min": 0.05,
                    "max": 1.0,
                    "description": "Fraction of main video width",
                },
            ],
        }
