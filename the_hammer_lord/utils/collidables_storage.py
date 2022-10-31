from __future__ import annotations  # for class C: def method(self, x: C)

import typing as tp

import pygame

from the_hammer_lord.entities.base import BaseEntity


class BoundingRect:
    def __init__(self, obj: BaseEntity):
        self.left_x = obj.x - obj.width // 2
        self.width = obj.width
        self.height = obj.height
        self.top_y = obj.y - obj.height // 2

    # TODO: add collision direction check (see MovementDir enum)
    def is_colliding_with(self, other: BoundingRect):
        return pygame.Rect.colliderect(
            pygame.Rect(self.left_x, self.top_y, self.width, self.height),
            pygame.Rect(other.left_x, other.top_y, other.width, other.height),
        )


# a class for storing all objects, capable of colliding with others
class CollidablesStorage:
    _objects: tp.List[BaseEntity] = []

    def extend(self, objects: tp.Iterable):
        self._objects.extend(objects)

    def can_move(self, character, dx, dy):
        character_box = BoundingRect(character)
        character_box.left_x += dx
        character_box.top_y += dy
        for obj in self._objects:
            if obj is character:
                continue
            if BoundingRect(obj).is_colliding_with(character_box):
                return False
        return True
