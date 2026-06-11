from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

from editor.base.filter_operation import FilterOperation
from editor.graph.filter_graph import FilterGraph


@dataclass
class SimpleVideoEffect(FilterOperation):
    """Base for effects expressible as a single static filter string.

    Subclasses only need to implement :meth:`filter_string` and
    :meth:`schema`. The graph threading is handled here.
    """

    @classmethod
    @abstractmethod
    def filter_string(cls) -> str:
        """Return the ffmpeg filter expression, e.g. ``'hue=s=0'``."""
        ...

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        out = graph.next_pad("v")
        graph.add_node(f"{video_in}{self.filter_string()}{out}")
        return out, audio_in

    @classmethod
    @abstractmethod
    def schema(cls) -> dict[str, Any]:
        ...
