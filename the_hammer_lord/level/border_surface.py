import logging
from enum import Enum, auto

from pygame import Rect, Surface, image, sprite

from the_hammer_lord.types import Point, Size2D
from the_hammer_lord.assets.sprites import SPRITES
from the_hammer_lord.utils.camera import Camera
from the_hammer_lord.utils.transform import fill_surface


class BorderSurfaceType(Enum):
    # from left to right
    FLOOR = auto()
    CEILING = auto()
    # from top to bottom
    LEFT_BORDER = auto()
    RIGHT_BORDER = auto()


class BorderSurface:
    # A visual representation for BorderSurfaceType.FLOOR/CEILING:
    #                   _______                                     _________
    #         __________       _________
    #   ______                          ____________________________
    _type: BorderSurfaceType
    _lvl_size: Size2D
    _forming_points: list[Point]
    # using sprite group instead of plain rects to render textures
    _collision_rects: sprite.Group
    _locked: bool = False
    # sprites texture
    _texture: Surface

    def __init__(
        self,
        surface_type: BorderSurfaceType,
        lvl_size: Size2D,
        forming_points_list: list[Point] = None,
    ):
        self._type = surface_type
        self._lvl_size = lvl_size
        self._texture = image.load(SPRITES["BrickTile"]).convert_alpha()
        self._collision_rects = sprite.Group()
        self._forming_points = []
        if forming_points_list:
            self.add_forming_points(forming_points_list)
            self.lock()

    def _form_rects(self):
        self._collision_rects.empty()
        for index, point in enumerate(self._forming_points):
            new_sprite = sprite.Sprite()

            cur_x, cur_y = 0, 0
            cur_w, cur_h = 0, 0

            match self._type:
                case BorderSurfaceType.FLOOR:
                    cur_w = self._calc_current_length(index, point)
                    cur_h = self._lvl_size[1] - point[1]
                    cur_x = point[0]
                    cur_y = point[1]

                case BorderSurfaceType.CEILING:
                    cur_w = self._calc_current_length(index, point)
                    cur_h = point[1]
                    cur_x = point[0]
                    cur_y = 0
                case BorderSurfaceType.LEFT_BORDER:
                    cur_w = point[0]
                    cur_h = self._calc_current_length(index, point)
                    cur_x = 0
                    cur_y = point[1]
                case BorderSurfaceType.RIGHT_BORDER:
                    cur_w = self._lvl_size[0] - point[0]
                    cur_h = self._calc_current_length(index, point)
                    cur_x = point[0]
                    cur_y = point[1]
                case _:
                    raise NotImplementedError

            new_sprite.rect = Rect((cur_x, cur_y), (cur_w, cur_h))
            new_sprite.image = fill_surface((cur_w, cur_h), self._texture)
            self._collision_rects.add(new_sprite)

    def _calc_current_length(self, index, point):
        # works with any type of surface (vertical/horizontal)
        # the result is used as height/weight depending on surface orientation
        is_last_forming_point = index == len(self._forming_points) - 1
        if self._type in (BorderSurfaceType.FLOOR, BorderSurfaceType.CEILING):
            axis = 0
        else:
            axis = 1
        return (
            # extend rectangle till the next forming point
            self._forming_points[index + 1][axis] - point[axis]
            if not is_last_forming_point
            # extend last forming_point till the end of the level
            else self._lvl_size[axis] - point[axis]
        )

    def add_forming_points(self, forming_points_list: list[Point]):
        if self._locked:
            logging.error(
                "The surface has been locked: no forming points can be added"
            )
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
                camera.calc_render_coords(
                    (rect_sprite.rect.x, rect_sprite.rect.y)
                ),
            )
