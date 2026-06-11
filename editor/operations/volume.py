from dataclasses import dataclass
from typing import Any

from editor.base.filter_operation import FilterOperation
from editor.graph.filter_graph import FilterGraph


@dataclass
class VolumeOperation(FilterOperation):
    """Adjusts the audio volume by a multiplier.

    Args:
        level: Volume multiplier. ``1.0`` = original, ``2.0`` = double,
               ``0.0`` = mute. Accepts values > 1.0 to amplify.
    """

    level: float = 1.0

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        out = graph.next_pad("a")
        graph.add_node(f"{audio_in}volume={self.level}{out}")
        return video_in, out  # video passes through unchanged

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "volume",
            "label": "Adjust Volume",
            "params": [
                {
                    "name": "level",
                    "type": "float",
                    "label": "Level",
                    "default": 1.0,
                    "min": 0.0,
                    "max": 10.0,
                    "description": "1.0 = original, 2.0 = double, 0.0 = mute",
                },
            ],
        }
