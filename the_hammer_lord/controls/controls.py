from abc import ABC, abstractmethod

from the_hammer_lord.types import Vector2D


class IControls(ABC):
    _motion_vector: Vector2D = [0, 0]
    _jumping: bool = False

    @property
    def motion_vector(self) -> Vector2D:
        return self._motion_vector

    @abstractmethod
    def get_input(self, *args, **kwargs):
        pass
