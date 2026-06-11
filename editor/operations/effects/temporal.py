from dataclasses import dataclass
from typing import Any

from editor.base.filter_operation import FilterOperation
from editor.graph.filter_graph import FilterGraph


@dataclass
class SpeedOperation(FilterOperation):
    """Changes playback speed for both video and audio.

    Args:
        factor: Speed multiplier. ``2.0`` = double speed, ``0.5`` = half speed.
                Audio uses ``atempo``, which is clamped to 0.5–2.0 by ffmpeg.

    Note:
        For factors outside 0.5–2.0 the audio filter needs to be chained
        (e.g. two atempo=2.0 nodes for 4x speed). This is not yet handled.
    """

    factor: float = 2.0

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        v_out = graph.next_pad("v")
        a_out = graph.next_pad("a")
        graph.add_node(f"{video_in}setpts=PTS/{self.factor}{v_out}")
        graph.add_node(f"{audio_in}atempo={self.factor}{a_out}")
        return v_out, a_out

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "speed",
            "label": "Speed",
            "params": [
                {"name": "factor", "type": "float", "label": "Factor", "default": 2.0, "min": 0.5, "max": 2.0},
            ],
        }


@dataclass
class FadeInOperation(FilterOperation):
    """Fades the video in from black at the start of the clip.

    Args:
        duration: Length of the fade in seconds. Default: 1.0.
    """

    duration: float = 1.0

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        out = graph.next_pad("v")
        graph.add_node(f"{video_in}fade=t=in:st=0:d={self.duration}{out}")
        return out, audio_in

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "fade_in",
            "label": "Fade In",
            "params": [
                {"name": "duration", "type": "float", "label": "Duration (s)", "default": 1.0, "min": 0.1, "max": 10.0},
            ],
        }


@dataclass
class FadeOutOperation(FilterOperation):
    """Fades the video out to black at a given point in the clip.

    Args:
        start:    Time in seconds at which the fade begins.
        duration: Length of the fade in seconds. Default: 1.0.
    """

    start: float
    duration: float = 1.0

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        out = graph.next_pad("v")
        graph.add_node(f"{video_in}fade=t=out:st={self.start}:d={self.duration}{out}")
        return out, audio_in

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "fade_out",
            "label": "Fade Out",
            "params": [
                {"name": "start", "type": "float", "label": "Start (s)", "default": 0.0, "min": 0.0},
                {"name": "duration", "type": "float", "label": "Duration (s)", "default": 1.0, "min": 0.1, "max": 10.0},
            ],
        }
