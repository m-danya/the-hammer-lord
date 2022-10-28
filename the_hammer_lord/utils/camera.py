from __future__ import annotations

import pygame
import typing as tp

from the_hammer_lord.types.movement import Vector2D

from the_hammer_lord.settings import *

# prevent cycle imports
if tp.TYPE_CHECKING:
    from the_hammer_lord.entities.player import Player


class Camera:
    x: float
    y: float
    player: tp.Optional[Player] = None

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def main(self, motion_vector: Vector2D):
        self.move(motion_vector)

    def move(self, motion_vector: Vector2D):
        # if player is bound, camera follows it
        if self.player:
            self.x, self.y = self.player.camera_adjusted_coords
            return

        # otherwise it moves independently of player
        # e.g. for cutscenes
        self.x += motion_vector[0] * CAMERA_SPEED
        self.y += motion_vector[1] * CAMERA_SPEED

    def get_object_coords(self, x: float, y: float) -> Vector2D:
        return x - self.x, y - self.y

    def bind_player(self, player: Player):
        self.player = player

    def unbind_player(self):
        self.player = None


def get_scaled_size(size: tuple[int, int]):
    return size[0] * SCALE_RATIO, size[1] * SCALE_RATIO


def scale_pixel_image(image: pygame.Surface):
    size = image.get_size()
    scaled = pygame.transform.scale(image, get_scaled_size(size))
    return scaled
