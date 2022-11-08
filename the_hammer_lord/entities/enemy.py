import pygame
import math

from the_hammer_lord.types import Point
from the_hammer_lord.entities.base import BaseEntity
from the_hammer_lord.settings import *
from the_hammer_lord.ui.health_bar import HealthBar


# TODO: class has to be refactored (extend DynamicEntity)
class BaseEnemy(BaseEntity):
    def __init__(self, x, y, target_for_chasing):
        # center coords
        self.x = x
        self.y = y
        self.target_for_chasing = target_for_chasing
        self.width = ENEMY_TEST_RECT_SIZE[0]
        self.height = ENEMY_TEST_RECT_SIZE[1]

        self.health_bar = HealthBar(ENEMY_HEALTH)
        self.health_bar.value //= 2

    def update(self):
        pass

    def move(self):
        pass

    def render(self, display: pygame.Surface, pos: Point):
        pass
