from pygame import Surface, image, transform

from the_hammer_lord.types import Size2D, Point, Vector2D
from the_hammer_lord.level.collision_surface import (
    CollisionSurface,
    SurfaceType,
)
from the_hammer_lord.entities.player import Player
from the_hammer_lord.ui.debug_info_corner import DebugInfoCorner
from the_hammer_lord.utils.camera import Camera
from the_hammer_lord.utils.transform import load_scaled_image
from the_hammer_lord.utils.collidables_storage import CollidablesStorage
from the_hammer_lord.lightning.light_map import LightMap
from the_hammer_lord.lightning.consts import COLOR_WARM_YELLOW, COLOR_WHITE


class Level:
    # top left corner is (0, 0) in level coordinate system
    _size: Size2D
    _floor: CollisionSurface
    _ceiling: CollisionSurface
    _camera: Camera
    _collidablesStorage: CollidablesStorage
    _player: Player
    _level_bg: Surface
    _lightmap: LightMap
    _debug_info_corner: DebugInfoCorner

    def __init__(self, level_size: Size2D = (3840, 1200)):
        self._size = level_size
        self._camera = Camera(1200, 88)
        self._collidablesStorage = CollidablesStorage()
        self._debug_info_corner = DebugInfoCorner(self)
        self._lightmap = LightMap(level_size)

    # generates the structure of the level, different params could be passed in the future
    def generate(self):
        self._level_bg = load_scaled_image("LevelBackground2", self._size)
        self._floor = CollisionSurface(SurfaceType.HORIZONTAL, self._size)
        self._floor.add_forming_points(
            [
                (0, 500),
                (420, 800),
                (800, 700),
                (1000, 600),
                (1200, 700),
                (1400, 800),
                (1700, 900),
                (1800, 1000),
                (1900, 1100),
                (2300, 1200),
            ]
        )
        self._floor.lock()
        self._collidablesStorage.extend([self._floor])

        self.spawn_player()

        # lightning setup
        for i in range(1, 10):
            self._lightmap.add_light_source((440 * i, 300), base_color=COLOR_WARM_YELLOW)
        self._lightmap.add_light_source(
            (self._player.rect.width, self._player.rect.height),
            base_color=COLOR_WHITE,
            waver=False,
            bound_to=self._player,
        )

    # creates new player on the level (could be used in reset)
    def spawn_player(self, pos: Point = (900, 400)):
        self._player = Player(pos)

    def setup(self, *args, **kwargs):
        self.generate()
        self._camera.bind_player(self._player)

    def reset(self):
        pass

    # called in the main event loop
    def update(self, display: Surface, motion_vector: Vector2D):
        # render level background
        display.blit(self._level_bg, self._camera.calc_render_coords((0, 0)))
        self._floor.render(display, self._camera)
        self._lightmap.apply(display, self._camera)
        self._player.update(
            display,
            self._camera.calc_render_coords((self._player.rect.x, self._player.rect.y)),
        )
        self._player.move(motion_vector, self._collidablesStorage)
        self._camera.detect_locked_axes(self._size)
        self._camera.move()
        self._debug_info_corner.update(display)
