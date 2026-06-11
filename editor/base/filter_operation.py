from abc import abstractmethod
from pathlib import Path
from typing import Any

from editor.base.operation import EditOperation
from editor.graph.filter_graph import FilterGraph


class FilterOperation(EditOperation):
    """Base for operations that contribute to a -filter_complex graph.

    All filter operations in a pipeline are composed into a single ffmpeg
    call. Each subclass implements :meth:`add_to_graph`, which appends one
    or more filter nodes and returns the updated (video_pad, audio_pad) names
    for the next operation in the chain.

    :meth:`apply` provides a standalone execution path for single-operation
    use — it builds a one-node graph and runs it directly.
    """

    @abstractmethod
    def add_to_graph(
        self,
        graph: FilterGraph,
        video_in: str,
        audio_in: str,
    ) -> tuple[str, str]:
        """Append filter node(s) to *graph* and return (video_out, audio_out) pads."""
        ...

    def apply(self, source: Path, output: Path) -> None:
        from editor.graph.runner import FFmpegRunner
        graph = FilterGraph()
        video_out, audio_out = self.add_to_graph(graph, "[0:v]", "[0:a]")
        FFmpegRunner().run_filter_graph(source, graph, output, video_out, audio_out)

    @classmethod
    @abstractmethod
    def schema(cls) -> dict[str, Any]:
        ...
