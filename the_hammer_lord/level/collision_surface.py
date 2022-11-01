import logging
from enum import Enum, auto

from pygame import Rect, Surface, image, sprite

from the_hammer_lord.types import Point
from the_hammer_lord.assets.sprites import SPRITES
from the_hammer_lord.utils.transform import scale_pixel_image


class SurfaceType(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


class CollisionSurface:
    _type: SurfaceType
    _width: int
    _height: int
    # by default, vertical surfaces are glued to the bottom of the screen, horizontal - to the left screen side;
    # this parameter changes this behaviour to the top of the screen and right screen side
    # for vertical and horizontal surfaces accordingly
    _reverse_mapping: bool = False
    _breakpoints: list[Point] = []
    # using sprite group instead of plain rects to render textures
    _collision_rects: sprite.Group = sprite.Group()
    _locked: bool = False
    # sprites texture
    _texture: Surface

    def __init__(self, surface_type: SurfaceType, width: int, height: int):
        self._type = surface_type
        self._height = height
        self._width = width
        self._texture = scale_pixel_image(image.load(SPRITES['Background']).convert_alpha())

    def _form_rects(self):
        self._collision_rects.empty()
        for index, point in enumerate(self._breakpoints):
            new_sprite = sprite.Sprite()
            new_sprite.image = self._texture

            last_breakpoint = index == len(self._breakpoints) - 1
            cur_x, cur_y = 0, 0
            cur_w, cur_h = 0, 0

            match self._type:
                case SurfaceType.HORIZONTAL:
                    # TODO: implement
                    pass
                case SurfaceType.VERTICAL:
                    # extend last breakpoint till the end of the surface
                    cur_w = self._breakpoints[index + 1][0] - cur_x if not last_breakpoint else self._width - cur_x
                    cur_h = point[1]
                    cur_x = point[0]
                    cur_y = cur_h
                    # TODO: add reverse_mapping checking

            new_sprite.rect = Rect((cur_x, cur_y), (cur_w, cur_h))
            self._collision_rects.add(new_sprite)

    def add_breakpoints(self, breakpoint_list: list[Point]):
        if self._locked:
            logging.warning('The surface has been locked: no breakpoints can be added')
            return

        self._breakpoints.extend(breakpoint_list)

    # locks the scene and enables collision testing, while restricting adding breakpoints
    def lock(self):
        self._locked = True
        # TODO: sorted list could be used for optimised collision checking
        #   by determining the closest breakpoint pair to the player's position
        self._breakpoints.sort()
        self._form_rects()

    # unlocks the scene and thus allows adding breakpoints, but disables collision testing
    def unlock(self):
        self._locked = False

    # TODO: maybe track rect collision as well in the future
    def collides_with(self, spr: sprite.Sprite) -> bool:
        if not self._locked:
            logging.error('Only locked surfaces can be used for collision tracking')
            return False

        # TODO: maybe we need to center ent.x and ent.y
        return sprite.spritecollideany(spr, self._collision_rects) is not None
