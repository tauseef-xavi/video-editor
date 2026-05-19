import tempfile
from pathlib import Path
from typing import List

from codec.strategies.base import CodecStrategy


class OptimizationPipeline:
    """Runs multiple :class:`CodecStrategy` instances in sequence.

    Each strategy's output becomes the next strategy's input. Intermediate
    files are written to a temporary directory and cleaned up automatically.
    Only the final stage writes to the caller-supplied ``output`` path.

    Example::

        pipeline = OptimizationPipeline([
            CRFReductionStrategy(crf=30),
            ScaleReductionStrategy(height=480),
            BitrateCapStrategy(video_bitrate="800k"),
        ])
        pipeline.run(Path("clip.mp4"), Path("clip_optimized.mp4"))

    Args:
        strategies: Ordered list of strategies to apply. Must not be empty.
    """

    def __init__(self, strategies: List[CodecStrategy]) -> None:
        if not strategies:
            raise ValueError("OptimizationPipeline requires at least one strategy.")
        self.strategies = strategies

    def run(self, source: Path, output: Path) -> None:
        if len(self.strategies) == 1:
            self.strategies[0].convert(source, output)
            return

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            current = source
            total = len(self.strategies)

            for i, strategy in enumerate(self.strategies):
                is_last = i == total - 1
                destination = output if is_last else tmp / f"stage_{i}.mp4"
                print(f"[pipeline] Stage {i + 1}/{total}: {strategy.__class__.__name__}")
                strategy.convert(current, destination)
                current = destination

        print(f"[pipeline] Done → {output}")
