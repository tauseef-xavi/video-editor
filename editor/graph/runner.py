import subprocess
from pathlib import Path

from editor.graph.filter_graph import FilterGraph

# Sentinel: pad was never routed through a filter node — map the raw stream instead.
_RAW_VIDEO = "[0:v]"
_RAW_AUDIO = "[0:a]"


class FFmpegRunner:
    """The single site that constructs and executes ffmpeg subprocesses."""

    def run_filter_graph(
        self,
        source: Path,
        graph: FilterGraph,
        output: Path,
        video_out: str,
        audio_out: str,
        output_args: list[str] | None = None,
    ) -> None:
        cmd = ["ffmpeg", "-y", "-i", str(source)]

        for extra in graph.extra_inputs:
            cmd += ["-i", str(extra)]

        cmd += ["-filter_complex", graph.build()]

        # Streams that were never touched by a filter are mapped directly from
        # the source input rather than through a named filter pad.
        cmd += ["-map", "0:v" if video_out == _RAW_VIDEO else video_out]
        cmd += ["-map", "0:a" if audio_out == _RAW_AUDIO else audio_out]

        if output_args:
            cmd += output_args

        cmd.append(str(output))

        print(f"[ffmpeg] {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg filter pass failed:\n{result.stderr}")
        print(f"[ffmpeg] Saved: {output}")
