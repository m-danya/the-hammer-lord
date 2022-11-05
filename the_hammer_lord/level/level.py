from pygame import Surface, image, transform

from the_hammer_lord.types import Size2D, Point, Vector2D
from the_hammer_lord.level.collision_surface import CollisionSurface, SurfaceType
from the_hammer_lord.entities.player import Player
from the_hammer_lord.utils.camera import Camera
from the_hammer_lord.utils.collidables_storage import CollidablesStorage
from the_hammer_lord.assets.sprites import SPRITES


class Level:
    # top left corner is (0, 0) in level coordinate system
    _size: Size2D
    _floor: CollisionSurface
    _ceiling: CollisionSurface
    _camera: Camera
    _collidables: CollidablesStorage = CollidablesStorage()
    _player: Player
    _level_bg: Surface

    def __init__(self, level_size: Size2D = (3840, 1200)):
        self._size = level_size
        self._camera = Camera(self._size[0] // 2, self._size[1] // 2)

    def _player_fits_screen(self) -> (bool, bool):
        cur_screen_shift = (self._camera.viewport_size[0] // 2, self._camera.viewport_size[1] // 2)
        return (self._player.x - cur_screen_shift[0] > 0 and self._player.x + cur_screen_shift[0] < self._size[0],
                self._player.y - cur_screen_shift[1] > 0 and self._player.y + cur_screen_shift[1] < self._size[1])

    # generates the structure of the level, different params could be passed in the future
    def generate(self):
        self._level_bg = image.load(SPRITES['LevelBackground1']).convert_alpha()
        self._level_bg = transform.scale(self._level_bg, self._size)
        self._floor = CollisionSurface(SurfaceType.VERTICAL, self._size)
        self._floor.add_breakpoints([(0, 500), (420, 800), (800, 700)])
        self._floor.lock()

    # creates new player on the level (could be used in reset)
    # FIXME: if player is spawned on the edge of the level, camera lags
    #  (change pos to 0, 500 to see)
    def spawn_player(self, pos: Point = (900, 400)):
        self._player = Player(pos)
        self._collidables.extend([self._player])

    def setup(self, *args, **kwargs):
        self.generate()
        self.spawn_player()

    def reset(self):
        pass

    # called in the main event loop
    def update(self, display: Surface, motion_vector: Vector2D):
        # render level background
        display.blit(self._level_bg, self._camera.calc_render_coords((0, 0)))

        self._floor.render(display, self._camera)
        self._player.update(display, self._camera.calc_render_coords(self._player.position))

        # FIXME: add proper collision checking
        x_collision, y_collision = self._floor.collides_with(self._player)
        self._player.move(motion_vector, y_collision)

        # a way to restrict camera from leaving level area
        x_fits, y_fits = self._player_fits_screen()
        if not x_fits or not y_fits:
            self._camera.unbind_player()
        elif x_fits and y_fits:
            self._camera.bind_player(self._player)

        # prevent camera from following user's input when unbound from player
        # TODO: add proper jump tracking for static camera using self._player.is_jumping()
        self._camera.move([0, 0])
