import pygame

from the_hammer_lord.types import Point
from the_hammer_lord.entities.base import StaticEntity
from the_hammer_lord.settings import HEALTH_BAR_THICKNESS


class HealthBar(StaticEntity):
    # TODO: add method for changing hp instead of constructing new class instances
    def __init__(self, value: int):
        super().__init__(dimensions=(int(value // 1.5), 10))
        # TODO: add typehinting for fields
        self.max_value = value
        self.value = value

    def render(self, display, pos: Point):
        # health bar border
        pygame.draw.rect(
            display,
            "black",
            pygame.Rect(
                (pos[0] - HEALTH_BAR_THICKNESS, pos[1] - HEALTH_BAR_THICKNESS),
                (
                    self.width + HEALTH_BAR_THICKNESS * 2,
                    self.height + HEALTH_BAR_THICKNESS * 2,
                ),
            ),
        )

        # health bar itself
        pygame.draw.rect(
            display,
            "red",
            pygame.Rect(pos, (self.width * self.value // self.max_value, self.height)),
        )
