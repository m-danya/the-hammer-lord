from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from pygame import Surface, Rect
from pygame.sprite import Sprite

from the_hammer_lord.types import Point, Size2D


@dataclass
class BaseEntity:
    # entity's top left coords
    # relative to the LEVEL coordinate system
    x: int
    y: int
    width: int
    height: int


class StaticEntity(ABC, BaseEntity, Sprite):
    def __init__(self, dimensions: Size2D, pos: Point = (0, 0)):
        super().__init__(x=pos[0], y=pos[1], width=dimensions[0], height=dimensions[1])
        # assign associated rectangle
        self.rect = Rect((self.x, self.y), (self.width, self.height))
        self.image = None

    @abstractmethod
    def render(self, display: Surface, pos: Point):
        pass


class DynamicEntity(StaticEntity):
    @abstractmethod
    def update(self, *args: Any, **kwargs: Any):
        pass
