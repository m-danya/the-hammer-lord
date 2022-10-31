from the_hammer_lord.types import Size2D

from the_hammer_lord.utils.collision_surface import CollisionSurface, SurfaceType
from the_hammer_lord.entities.player import Player


class Level:
    # TODO: maybe add reference to the Player and Camera
    _size: Size2D
    _floor: CollisionSurface
    _ceiling: CollisionSurface

    def __init__(self, level_size: Size2D = (1920, 1080)):
        self._size = level_size

    # generates the structure of the level, different params could be passed in the future
    def generate(self):
        self._floor = CollisionSurface(SurfaceType.VERTICAL, self._size[0], self._size[1])
        self._floor.add_breakpoints([(0, 180)])
        self._floor.lock()

    # creates new player on the level (could be used in reset)
    def spawn_player(self) -> Player:
        pass

    def reset(self):
        pass

    # will be called in the main event loop
    def render_scene(self):
        pass




