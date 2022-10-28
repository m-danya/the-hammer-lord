import pygame

from the_hammer_lord.settings import *
from the_hammer_lord.global_ctx import camera


class HealthBar:
    def __init__(self, value):
        self.max_value = value
        self.value = value
        self.height = 10
        self.width = self.max_value // 1.5

    def render(self, display, x, y):
        pygame.draw.rect(
            display,
            "black",
            pygame.Rect(
                *camera.get_object_coords(
                    x - self.width // 2 - HEALTH_BAR_THICKNESS,
                    y - self.height // 2 - HEALTH_BAR_THICKNESS,
                ),
                self.width + HEALTH_BAR_THICKNESS * 2,
                self.height + HEALTH_BAR_THICKNESS * 2
            ),
        )
        pygame.draw.rect(
            display,
            "red",
            pygame.Rect(
                *camera.get_object_coords(
                    x - self.width // 2,
                    y - self.height // 2,
                ),
                self.width * self.value // self.max_value,
                self.height
            ),
        )
