import math

from pygame.color import Color

from the_hammer_lord.lightning.consts import ALPHA_OPAQUE


def linear_color_fade(original: Color, degree: float) -> Color:
    if degree < 0 or degree > 1:
        raise ValueError("Fade degree must be specified in [0, 1] range")

    faded = Color(0, 0, 0)
    faded.r = math.floor(original.r * degree)
    faded.g = math.floor(original.g * degree)
    faded.b = math.floor(original.b * degree)

    return faded


def linear_color_alpha_fade(original: Color, degree: float) -> Color:
    if degree < 0 or degree > 1:
        raise ValueError("Fade degree must be specified in [0, 1] range")

    faded = Color(original)
    faded.a = math.floor(ALPHA_OPAQUE * degree)
    return faded
