import tempfile
from pathlib import Path
from typing import List

from editor.base.filter_operation import FilterOperation
from editor.base.operation import EditOperation
from editor.base.stream_operation import StreamOperation
from editor.graph.filter_graph import FilterGraph
from editor.graph.runner import FFmpegRunner


class EditorPipeline:
    """Orchestrates a sequence of :class:`EditOperation` instances.

    Execution is split into two tiers:

    1. **Stream tier** — :class:`StreamOperation` instances run first via
       ``apply()``, using stream copy so no quality is lost.
    2. **Filter tier** — all :class:`FilterOperation` instances are composed
       into a single ``-filter_complex`` pass by :class:`FFmpegRunner`,
       regardless of how many operations are in the chain.

    This means N filter operations still produce exactly one re-encode.

    Example::

        pipeline = EditorPipeline([
            TrimOperation("0:30", "1:00"),
            FlipOperation("horizontal"),
            TextOverlayOperation("Hello", color="yellow"),
            VolumeOperation(1.5),
        ])
        pipeline.run(Path("source.mp4"), Path("result.mp4"))

    Args:
        operations: Ordered list of operations. Must not be empty.
    """

    def __init__(self, operations: List[EditOperation]) -> None:
        if not operations:
            raise ValueError("EditorPipeline requires at least one operation.")
        self.operations = operations

    def run(self, source: Path, output: Path) -> None:
        stream_ops = [op for op in self.operations if isinstance(op, StreamOperation)]
        filter_ops = [op for op in self.operations if isinstance(op, FilterOperation)]

        with tempfile.TemporaryDirectory() as tmp:
            current = source

            if stream_ops:
                stream_dest = Path(tmp) / "after_stream.mp4" if filter_ops else output
                prev = current
                total = len(stream_ops)
                for i, op in enumerate(stream_ops):
                    is_last = i == total - 1
                    dest = stream_dest if is_last else Path(tmp) / f"stream_{i}.mp4"
                    print(f"[editor] Stream {i + 1}/{total}: {op.__class__.__name__}")
                    op.apply(prev, dest)
                    prev = dest
                current = stream_dest

            if filter_ops:
                graph = FilterGraph()
                video_pad, audio_pad = "[0:v]", "[0:a]"
                for op in filter_ops:
                    video_pad, audio_pad = op.add_to_graph(graph, video_pad, audio_pad)
                print(f"[editor] Filter pass: {', '.join(op.__class__.__name__ for op in filter_ops)}")
                FFmpegRunner().run_filter_graph(current, graph, output, video_pad, audio_pad)

        print(f"[editor] Done → {output}")
