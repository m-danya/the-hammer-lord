from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from pygame import Surface, Rect
from pygame.sprite import Sprite

from the_hammer_lord.types import Point, Size2D


class Entity(ABC, Sprite):
    def __init__(self, dimensions: Size2D, position: Point = (0, 0)):
        super().__init__()
        # assign associated rectangle
        self.rect = Rect((position[0], position[1]), (dimensions[0], dimensions[1]))
        self.image = None

    @abstractmethod
    def render(self, display: Surface, pos: Point):
        pass
