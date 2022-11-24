from __future__ import annotations  # for class C: def method(self, x: C)

import typing as tp

from pygame.sprite import Group, Sprite, spritecollide

from the_hammer_lord.level.border_surface import BorderSurface


# a class for storing all objects, capable of colliding with others
class CollidablesStorage:
    _objects: list[any]

    def __init__(self):
        self._objects = []

    def extend(self, objects: tp.Iterable):
        self._objects.extend(objects)

    def _get_sprites(self):
        # dynamically get sprites from all stored objects, because they may have
        # changes, e.g. BorderSurface got a new forming point
        sprites = Group()
        for collidables in self._objects:
            match collidables:
                case BorderSurface():
                    sprites.add(collidables.get_sprites())
                case Group():
                    sprites.add(collidables)
                case Sprite():
                    sprites.add(collidables)
                case _:
                    raise NotImplementedError
        return sprites

    def get_collided_sprites_with(self, sprite):
        return spritecollide(sprite, self._get_sprites(), False)
