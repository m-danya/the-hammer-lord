import pygame
import math

from the_hammer_lord.entities.base import BaseEntity

from the_hammer_lord.settings import *
from the_hammer_lord.ui.health_bar import HealthBar

from the_hammer_lord.global_ctx import camera, collidablesStorage


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

    def main(self, display: pygame.Surface):
        self.move()
        self.render(display)

    def move(self):
        # check whether the enemy sees a player
        x_dist = self.target_for_chasing.x - self.x
        y_dist = self.target_for_chasing.y - self.y
        dx = math.copysign(ENEMY_SPEED, x_dist)
        dy = math.copysign(ENEMY_SPEED, y_dist)
        distance = math.hypot(x_dist, y_dist)
        # TODO: change logic to avoid collision with any
        #  character in the game
        #  (instead of 200 < distance).
        #  smth like every character will call
        #  can_move_here(..) before actually moving
        if distance < 500 and collidablesStorage.can_move(self, dx, dy):
            # move toward the chasing target
            self.x += dx
            self.y += dy

    def render(self, display: pygame.Surface):
        # enemy is a composition of 2 rectangles for now
        pygame.draw.rect(
            display,
            "darkblue",
            pygame.Rect(
                *camera.get_object_coords(
                    self.x - ENEMY_TEST_RECT_SIZE[0] // 2,
                    self.y - ENEMY_TEST_RECT_SIZE[1] // 2,
                ),
                *ENEMY_TEST_RECT_SIZE,
            ),
        )
        pygame.draw.rect(
            display,
            "red",
            pygame.Rect(
                *camera.get_object_coords(
                    self.x,
                    self.y,
                ),
                ENEMY_TEST_RECT_SIZE[0] // 2,
                ENEMY_TEST_RECT_SIZE[0] // 2,
            ),
        )

        self.health_bar.render(
            display, self.x, self.y - ENEMY_TEST_RECT_SIZE[1] // 2 - 30
        )
