from pygame import Surface, transform

from the_hammer_lord.settings import SCALE_RATIO


def get_scaled_size(size: tuple[int, int]):
    return size[0] * SCALE_RATIO, size[1] * SCALE_RATIO


def scale_pixel_image(image: Surface):
    size = image.get_size()
    scaled = transform.scale(image, get_scaled_size(size))
    return scaled
