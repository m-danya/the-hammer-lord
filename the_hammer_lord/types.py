import typing as tp
from enum import Enum, auto
from dataclasses import dataclass


Size2D = tuple[int, int]
Vector2D = list[float, float]
Point = tuple[int, int]


@dataclass
class Animation:
    sprite_path: str
    frames_cnt: int


class MovementDir(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class PlayerAction(Enum):
    IDLE = auto()
