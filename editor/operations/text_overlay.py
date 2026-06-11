from dataclasses import dataclass, field
from typing import Any

from editor.base.filter_operation import FilterOperation
from editor.graph.filter_graph import FilterGraph


def _escape(text: str) -> str:
    """Escape characters that ffmpeg drawtext treats as special."""
    return text.replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")


@dataclass
class TextOverlayOperation(FilterOperation):
    """Burns text onto the video using ffmpeg's drawtext filter.

    Args:
        text:      The string to render.
        x:         Horizontal position expression (ffmpeg geometry). Default: centred.
        y:         Vertical position expression. Default: 10px from the bottom.
        font_size: Font size in points. Default: 36.
        color:     Font colour name or hex (e.g. ``"white"``, ``"#ff0000"``). Default: ``"white"``.
    """

    text: str
    x: str = "(w-text_w)/2"
    y: str = "h-th-10"
    font_size: int = 36
    color: str = "white"

    def add_to_graph(self, graph: FilterGraph, video_in: str, audio_in: str) -> tuple[str, str]:
        out = graph.next_pad("v")
        filter_str = (
            f"drawtext=text='{_escape(self.text)}'"
            f":x={self.x}:y={self.y}"
            f":fontsize={self.font_size}:fontcolor={self.color}"
        )
        graph.add_node(f"{video_in}{filter_str}{out}")
        return out, audio_in

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {
            "name": "text_overlay",
            "label": "Text Overlay",
            "params": [
                {"name": "text", "type": "string", "label": "Text", "default": ""},
                {"name": "x", "type": "string", "label": "X position", "default": "(w-text_w)/2"},
                {"name": "y", "type": "string", "label": "Y position", "default": "h-th-10"},
                {"name": "font_size", "type": "int", "label": "Font size", "default": 36, "min": 8, "max": 200},
                {"name": "color", "type": "string", "label": "Color", "default": "white"},
            ],
        }
