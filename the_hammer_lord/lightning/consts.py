from enum import Enum, auto

from pygame.color import Color

ALPHA_OPAQUE = 255
ALPHA_TRANSPARENT = 0

TORCH_DIMENSIONS = (35, 75)

COLOR_WARM_YELLOW = Color(255, 220, 0)
COLOR_WHITE = Color(255, 255, 255)


class ProgressionType(Enum):
    LINEAR = auto()
    QUADRATIC = auto()
