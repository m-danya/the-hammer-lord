from enum import Enum, auto


Vector2D = [float, float]


class MovementDir(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
