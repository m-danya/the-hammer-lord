from abc import ABC, abstractmethod

from the_hammer_lord.types import Vector2D
from the_hammer_lord.settings import GRAVITY_FORCE


class IControls(ABC):
    _motion_vector: Vector2D = [0, 0]
    _jumping: bool = False

    @property
    def motion_vector(self) -> Vector2D:
        return self._motion_vector

    def in_air(self):
        return self._motion_vector[1] != 0

    def is_jumping(self):
        return self._jumping

    def apply_gravity(self):
        if not self.in_air():
            self._jumping = False
        else:
            # TODO: calc correctly
            self._motion_vector[1] += GRAVITY_FORCE

    @abstractmethod
    def handle_movement(self, *args, **kwargs):
        pass
