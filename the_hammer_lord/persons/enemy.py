import pygame
import math
from the_hammer_lord.settings import *


class BaseEnemy:
    def __init__(self, x, y, target_for_chasing):
        # center coords
        self.x = x
        self.y = y
        self.target_for_chasing = target_for_chasing

    def main(self, display: pygame.Surface):
        self.move()
        self.render(display)

    def move(self):
        # check whether the enemy sees a player
        dx = self.target_for_chasing.x - self.x
        dy = self.target_for_chasing.y - self.y
        distance = math.hypot(dx, dy)
        # TODO: change logic to avoid collision with any
        #  character in the game
        #  (instead of 200 < distance).
        #  smth like every character will call
        #  can_move_here(..) before actually moving
        if 200 < distance < 500:
            # move toward the chasing target
            self.x += math.copysign(ENEMY_SPEED, dx)
            self.y += math.copysign(ENEMY_SPEED, dy)

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
