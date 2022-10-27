import pygame
from abc import ABC, abstractmethod


class Controls(ABC):
    _motion_vector: [float, float]

    def __init__(self):
        self._motion_vector = [0, 0]

    @property
    def motion_vector(self) -> [float, float]:
        return self._motion_vector

    @abstractmethod
    def handle_movement(self, *args, **kwargs):
        pass

