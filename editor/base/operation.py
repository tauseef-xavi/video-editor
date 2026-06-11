from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class EditOperation(ABC):
    """Base class for all editing operations.

    Subclasses are dataclasses whose fields are the operation's parameters.
    Each subclass must implement :meth:`apply` and :meth:`schema`.
    """

    @abstractmethod
    def apply(self, source: Path, output: Path) -> None:
        """Apply this operation to *source* and write the result to *output*."""
        ...

    @classmethod
    @abstractmethod
    def schema(cls) -> dict[str, Any]:
        """Return a descriptor a UI can use to render a form for this operation.

        Structure::

            {
                "name": "trim",
                "label": "Trim Clip",
                "params": [
                    {
                        "name": "start",
                        "type": "timestamp",
                        "label": "Start time",
                        "default": "0:00",
                    },
                    ...
                ],
            }
        """
        ...
