import logging
from enum import Enum, auto

from pygame import Rect, Surface, image, sprite

from the_hammer_lord.types import Point, Size2D
from the_hammer_lord.assets.sprites import SPRITES
from the_hammer_lord.utils.camera import Camera
from the_hammer_lord.utils.transform import fill_surface


class SurfaceType(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


class CollisionSurface:
    # A visual representation for some SurfaceType.HORIZONTAL CollisionSurface:
    #                   _______                                     _________
    #         __________       _________
    #   ______                          ____________________________
    _type: SurfaceType
    _lvl_size: Size2D
    _forming_points: list[Point]
    # using sprite group instead of plain rects to render textures
    _collision_rects: sprite.Group = sprite.Group()
    _locked: bool = False
    # sprites texture
    _texture: Surface

    def __init__(self, surface_type: SurfaceType, lvl_size: Size2D):
        self._type = surface_type
        self._lvl_size = lvl_size
        self._forming_points = []
        self._texture = image.load(SPRITES["BrickTile"]).convert_alpha()

    def _form_rects(self):
        self._collision_rects.empty()
        for index, point in enumerate(self._forming_points):
            new_sprite = sprite.Sprite()

            is_last_forming_point = index == len(self._forming_points) - 1
            cur_x, cur_y = 0, 0
            cur_w, cur_h = 0, 0

            match self._type:
                case SurfaceType.VERTICAL:
                    # walls
                    # TODO: implement
                    pass
                case SurfaceType.HORIZONTAL:
                    # floors / ceilings
                    # TODO: move this and future logic to a separate function (e.g. add_joint(forming_point: Point))
                    # extend last forming_point till the end of the surface
                    cur_w = (
                        self._forming_points[index + 1][0] - point[0]
                        if not is_last_forming_point
                        else self._lvl_size[0] - point[0]
                    )
                    cur_h = self._lvl_size[1] - point[1]
                    cur_x = point[0]
                    cur_y = point[1]
            new_sprite.rect = Rect((cur_x, cur_y), (cur_w, cur_h))
            new_sprite.image = fill_surface((cur_w, cur_h), self._texture)
            self._collision_rects.add(new_sprite)

    def add_forming_points(self, forming_points_list: list[Point]):
        if self._locked:
            logging.error("The surface has been locked: no forming points can be added")
            return

        self._forming_points.extend(forming_points_list)

    # locks the scene and enables collision testing, while restricting adding forming points
    def lock(self):
        self._locked = True
        # TODO: sorted list could be used for optimised collision checking
        #   by determining the closest forming point pair to the player's position
        self._forming_points.sort()
        self._form_rects()

    # unlocks the scene and thus allows adding forming points, but disables collision testing
    def unlock(self):
        self._locked = False

    def get_sprites(self):
        return self._collision_rects.sprites()

    def render(self, display: Surface, camera: Camera):
        if not self._locked:
            logging.error("Only locked surfaces can be rendered")
            return

        for rect_sprite in self._collision_rects.sprites():
            display.blit(
                rect_sprite.image,
                camera.calc_render_coords((rect_sprite.rect.x, rect_sprite.rect.y)),
            )
