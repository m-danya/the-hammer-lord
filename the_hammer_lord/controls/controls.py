from abc import ABC, abstractmethod

from the_hammer_lord.types.movement import Vector2D


class Controls(ABC):
    _motion_vector: Vector2D

    def __init__(self):
        self._motion_vector = [0, 0]

    @property
    def motion_vector(self) -> Vector2D:
        return self._motion_vector

    @abstractmethod
    def handle_movement(self, *args, **kwargs):
        pass

