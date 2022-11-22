from math import ceil

from pygame import Surface, transform, image

from the_hammer_lord.types import Size2D
from the_hammer_lord.assets.sprites import SPRITES
from the_hammer_lord.settings import SCALE_RATIO


def load_scaled_image(sprite_name: str, size: Size2D) -> Surface:
    img = image.load(SPRITES[sprite_name]).convert_alpha()
    img = transform.scale(img, size)
    return img


def get_scaled_size(size: tuple[int, int]):
    return size[0] * SCALE_RATIO, size[1] * SCALE_RATIO


def scale_pixel_image(img: Surface):
    size = img.get_size()
    scaled = transform.scale(img, get_scaled_size(size))
    return scaled


# creates a surface of given size with the filled with the repeated tiles
def fill_surface(size: Size2D, tile: Surface) -> Surface:
    tile_sz = tile.get_size()
    filled_surface = Surface(size)
    for y_shift in range(ceil(size[1] / tile_sz[1])):
        for x_shift in range(ceil(size[0] / tile_sz[0])):
            filled_surface.blit(tile, (x_shift * tile_sz[0], y_shift * tile_sz[1]))

    return filled_surface
