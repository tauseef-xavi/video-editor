from abc import ABC, abstractmethod
from pathlib import Path


class CodecStrategy(ABC):
    @abstractmethod
    def convert(self, source: Path, output: Path) -> None:
        """Re-encode source into output using this strategy's codec settings."""
        ...
