from __future__ import annotations  # for class C: def method(self, x: C)

import typing as tp

import pygame

from the_hammer_lord.level.collision_surface import CollisionSurface


# a class for storing all objects, capable of colliding with others
class CollidablesStorage:
    objects: list[any] = []

    def extend(self, objects: tp.Iterable):
        self.objects.extend(objects)
