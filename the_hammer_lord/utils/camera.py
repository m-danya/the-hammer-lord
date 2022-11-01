from __future__ import annotations

import typing as tp

from the_hammer_lord.types import Vector2D, Point
from the_hammer_lord.entities.base import BaseEntity
from the_hammer_lord.settings import *

# prevent cycle imports
if tp.TYPE_CHECKING:
    from the_hammer_lord.entities.player import Player


class Camera:
    # coords of the center of a viewport
    # relative to the LEVEL coordinate system
    x: int
    y: int
    _player: tp.Optional[Player] = None
    _scale_factor: float = 1

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # could be used for zooming scene in / out
    def scale(self, scale_factor: float):
        self._scale_factor = scale_factor

    def move(self, motion_vector: Vector2D):
        # if player is bound, camera follows it
        if self._player:
            self.x, self.y = self._player.x, self._player.y
            return

        # otherwise it moves independently of player
        # e.g. for cutscenes
        self.x += motion_vector[0] * CAMERA_SPEED
        self.y += motion_vector[1] * CAMERA_SPEED

    def calc_render_coords(self, ent: BaseEntity) -> Point:
        return ((SCREEN_SIZE[0] * self._scale_factor) // 2 + ent.x - self.x,
                (SCREEN_SIZE[1] * self._scale_factor) // 2 + ent.y - self.y)

    def bind_player(self, player: Player):
        self._player = player
        self.x = player.x
        self.y = player.y

    def unbind_player(self):
        self._player = None
