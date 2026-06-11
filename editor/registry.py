from typing import Type

from editor.base.operation import EditOperation
from editor.operations.flip import FlipOperation
from editor.operations.pip import PictureInPictureOperation
from editor.operations.text_overlay import TextOverlayOperation
from editor.operations.trim import TrimOperation
from editor.operations.volume import VolumeOperation

REGISTRY: dict[str, Type[EditOperation]] = {
    "trim": TrimOperation,
    "flip": FlipOperation,
    "volume": VolumeOperation,
    "text_overlay": TextOverlayOperation,
    "pip": PictureInPictureOperation,
}


def schemas() -> list[dict]:
    """Return the schema for every registered operation. Intended for UI consumers."""
    return [cls.schema() for cls in REGISTRY.values()]
