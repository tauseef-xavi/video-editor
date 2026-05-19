from abc import ABC, abstractmethod
from pathlib import Path


class Editor(ABC):
    @abstractmethod
    def edit(self, source: Path, output: Path) -> None:
        """Apply an editing operation to *source* and write the result to *output*."""
        ...
