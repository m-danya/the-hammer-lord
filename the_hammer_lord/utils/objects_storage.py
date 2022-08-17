from __future__ import annotations  # for class C: def method(self, x: C)

import typing

import pygame


class ObjectBox:
    def __init__(self, obj):
        self.left_x = obj.x - obj.width // 2
        self.width = obj.width
        self.height = obj.height
        self.top_y = obj.y - obj.height // 2

    def is_colliding_with(self, other: ObjectBox):
        return pygame.Rect.colliderect(
            pygame.Rect(self.left_x, self.top_y, self.width, self.height),
            pygame.Rect(other.left_x, other.top_y, other.width, other.height),
        )


class ObjectsStorage:
    # a class for storing all objects, capable of colliding with others
    def __init__(self):
        self.objects = []

    def extend(self, objects: typing.Iterable):
        self.objects.extend(objects)

    def can_move(self, character, dx, dy):
        character_box = ObjectBox(character)
        character_box.left_x += dx
        character_box.top_y += dy
        for obj in self.objects:
            if obj is character:
                continue
            if ObjectBox(obj).is_colliding_with(character_box):
                return False
        return True
