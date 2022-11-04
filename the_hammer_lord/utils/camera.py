from __future__ import annotations

import typing as tp
from math import floor

from the_hammer_lord.types import Vector2D, Point, Size2D
from the_hammer_lord.settings import CAMERA_SPEED, SCREEN_SIZE

# prevent cycle imports
if tp.TYPE_CHECKING:
    from the_hammer_lord.entities.player import Player


class Camera:
    # coords of the center of a viewport
    # relative to the LEVEL coordinate system
    x: int
    y: int
    _player: tp.Optional[Player] = None
    _viewport_size: Size2D = SCREEN_SIZE

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def viewport_size(self) -> Size2D:
        return self._viewport_size

    # could be used for zooming scene in / out
    def set_viewport_size(self, size: Size2D):
        self._viewport_size = size

    def move(self, motion_vector: Vector2D):
        # if player is bound, camera follows it
        if self._player:
            self.x, self.y = self._player.x, self._player.y
            return

        # otherwise it moves independently of player
        # e.g. for cutscenes
        self.x += floor(motion_vector[0] * CAMERA_SPEED)
        self.y += floor(motion_vector[1] * CAMERA_SPEED)

    @property
    def viewport_area(self) -> (Point, Point):
        scaled_screen_shift = (self._viewport_size[0] // 2, self._viewport_size[1] // 2)
        return ((self.x - scaled_screen_shift[0], self.y - scaled_screen_shift[1]),
                (self.x + scaled_screen_shift[0], self.y + scaled_screen_shift[1]))

    def calc_render_coords(self, ent_coords: Point) -> Point:
        return (self._viewport_size[0] // 2 + ent_coords[0] - self.x,
                self._viewport_size[1] // 2 + ent_coords[1] - self.y)

    def bind_player(self, player: Player):
        self._player = player

    def unbind_player(self):
        self._player = None
