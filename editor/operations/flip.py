from dataclasses import dataclass
from typing import Any, Literal

from editor.base.filter_operation import FilterOperation
from editor.graph.filter_graph import FilterGraph


@dataclass
class FlipOperation(FilterOperation):
    """Flips the video horizontally or vertically.

    Args:
        direction: ``"horizontal"`` (mirror left-right) or ``"vertical"`` (flip upside-down).
    """

    direction: Literal["horizontal", "vertical"] = "horizontal"

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        f = "hflip" if self.direction == "horizontal" else "vflip"
        out = graph.next_pad("v")
        graph.add_node(f"{video_in}{f}{out}")
        return out, audio_in

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "flip",
            "label": "Flip Video",
            "params": [
                {
                    "name": "direction",
                    "type": "enum",
                    "label": "Direction",
                    "options": ["horizontal", "vertical"],
                    "default": "horizontal",
                },
            ],
        }
