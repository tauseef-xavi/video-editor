from pathlib import Path


class FilterGraph:
    """Assembles an ffmpeg -filter_complex expression.

    Operations call :meth:`add_node` to register filter strings and
    :meth:`next_pad` to get unique pad label names. Extra input files
    (e.g. a PiP overlay) are registered via :meth:`add_input`, which
    returns the input stream index (0 is always the main source).
    """

    def __init__(self) -> None:
        self._nodes: list[str] = []
        self._extra_inputs: list[Path] = []
        self._pad_counters: dict[str, int] = {}

    def add_node(self, node: str) -> None:
        self._nodes.append(node)

    def add_input(self, path: Path) -> int:
        """Register an additional -i input. Returns its stream index (1-based)."""
        self._extra_inputs.append(path)
        return len(self._extra_inputs)  # index 0 is the main source

    def next_pad(self, prefix: str = "v") -> str:
        """Return the next unique pad label, e.g. '[v0]', '[a1]', '[pip0]'."""
        n = self._pad_counters.get(prefix, 0)
        self._pad_counters[prefix] = n + 1
        return f"[{prefix}{n}]"

    @property
    def extra_inputs(self) -> list[Path]:
        return list(self._extra_inputs)

    def build(self) -> str:
        return ";".join(self._nodes)
