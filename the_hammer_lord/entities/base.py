from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from pygame import Surface, Rect
from pygame.sprite import Sprite

from the_hammer_lord.types import Point, Size2D


# TODO: get rid of this class and instead
#   add @property mappings to sprite.rect props in StaticEntity
@dataclass
class BaseEntity:
    # entity's top left coords
    # relative to the LEVEL coordinate system
    x: int
    y: int
    width: int
    height: int

    @property
    def position(self) -> Point:
        return self.x, self.y


class StaticEntity(ABC, BaseEntity, Sprite):
    def __init__(self, dimensions: Size2D, pos: Point = (0, 0)):
        super().__init__(x=pos[0], y=pos[1], width=dimensions[0], height=dimensions[1])
        # assign associated rectangle
        self.rect = Rect((self.x, self.y), (self.width, self.height))
        self.image = None

    def get_collision_sides(self, other: StaticEntity) -> (bool, bool, bool, bool):
        collisions = (False, False, False, False)

        if not other:
            return collisions

        # TODO: implement: https://youtu.be/1_H7InPMjaY?t=268
        return collisions

    @abstractmethod
    def render(self, display: Surface, pos: Point):
        pass


# TODO: maybe move method should be added as well...
class DynamicEntity(StaticEntity):
    @abstractmethod
    def update(self, *args: Any, **kwargs: Any):
        pass
