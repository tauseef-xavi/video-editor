from typing import Type

from editor.base.operation import EditOperation
from editor.operations.effects import (
    BlurOperation,
    BrightnessOperation,
    FadeInOperation,
    FadeOutOperation,
    GrayscaleOperation,
    SaturationOperation,
    SepiaOperation,
    SharpenOperation,
    SpeedOperation,
    VignetteOperation,
)
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
    "grayscale": GrayscaleOperation,
    "sepia": SepiaOperation,
    "brightness": BrightnessOperation,
    "saturation": SaturationOperation,
    "blur": BlurOperation,
    "sharpen": SharpenOperation,
    "vignette": VignetteOperation,
    "speed": SpeedOperation,
    "fade_in": FadeInOperation,
    "fade_out": FadeOutOperation,
}


def schemas() -> list[dict]:
    """Return the schema for every registered operation. Intended for UI consumers."""
    return [cls.schema() for cls in REGISTRY.values()]
