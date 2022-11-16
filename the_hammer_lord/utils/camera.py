from __future__ import annotations

import typing as tp
from math import floor

from the_hammer_lord.types import Vector2D, Point, Size2D
from the_hammer_lord.settings import CAMERA_SPEED, SCREEN_SIZE

# prevent cycle imports
if tp.TYPE_CHECKING:
    from the_hammer_lord.entities.player import Player


class Camera:
    # coords of top left corner of a viewport
    # relative to the LEVEL coordinate system
    x: int
    y: int
    _player: tp.Optional[Player] = None
    _viewport_size: Size2D = SCREEN_SIZE

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self._lock_x = False
        self._lock_y = False

    @property
    def viewport_size(self) -> Size2D:
        return self._viewport_size

    # could be used for zooming scene in / out
    def set_viewport_size(self, size: Size2D):
        self._viewport_size = size

    def detect_locked_axes(self, lvl_size):
        x_fits, y_fits = (
            (
                self._player.rect.centerx - self.viewport_size[0] // 2 > 0
                and self._player.rect.centerx + self.viewport_size[0] < lvl_size[0]
            ),
            (
                self._player.rect.centery - self.viewport_size[1] // 2 > 0
                and self._player.rect.centery + self.viewport_size[1] // 2 < lvl_size[1]
            ),
        )
        # y-axis is locked when player is jumping
        y_fits = y_fits and self._player.is_on_land
        self._lock_x = not x_fits
        self._lock_y = not y_fits

    @staticmethod
    def move_to_target(target_x: int, current_x: int):
        # slowly move closer to the player (e.g. when he jumped on something)
        difference = target_x - current_x
        if abs(difference) > 1:  # if player is too far
            sign = 1 if difference > 0 else -1
            # move towards the player not faster than CAMERA_SPEED
            return current_x + sign * min(abs(difference), CAMERA_SPEED)
        # otherwise just teleport
        return target_x

    def move(self, motion_vector: Vector2D = (0, 0)):
        # if player is bound, camera can follow it, if axis are not locked
        if self._player:
            if not self._lock_x:
                target_x = self._player.rect.centerx - self.viewport_size[0] // 2
                self.x = self.move_to_target(target_x, self.x)
            if not self._lock_y:
                target_y = self._player.rect.centery - self.viewport_size[1] // 2
                self.y = self.move_to_target(target_y, self.y)

            return

        # otherwise it moves independently of player
        # e.g. for cutscenes
        # for now, unbinding is not used at all
        pass

    @property
    def viewport_area(self) -> (Point, Point):
        return (
            (self.x, self.y),
            (self.x + self._viewport_size[0], self.y + self._viewport_size[1]),
        )

    def calc_render_coords(self, object_coords: Point) -> Point:
        return (
            object_coords[0] - self.x,
            object_coords[1] - self.y,
        )

    def bind_player(self, player: Player):
        self._player = player

    def unbind_player(self):
        self._player = None
