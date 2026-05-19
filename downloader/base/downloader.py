from abc import ABC, abstractmethod
from pathlib import Path


class Downloader(ABC):
    @abstractmethod
    def download(self, url: str, output_path: Path) -> None:
        """Download content from *url* and save it to *output_path*."""
        ...
