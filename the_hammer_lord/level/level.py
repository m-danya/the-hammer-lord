from pathlib import Path
from pygame import Surface, image

from the_hammer_lord.types import Size2D, Point, Vector2D
from the_hammer_lord.level.collision_surface import CollisionSurface, SurfaceType
from the_hammer_lord.entities.base import BaseEntity
from the_hammer_lord.entities.player import Player
from the_hammer_lord.utils.camera import Camera
from the_hammer_lord.utils.transform import scale_pixel_image, get_scaled_size
from the_hammer_lord.utils.collidables_storage import CollidablesStorage


class Level:
    # top left corner is (0, 0) in level coordinate system
    _size: Size2D
    _floor: CollisionSurface
    _ceiling: CollisionSurface
    _camera: Camera = Camera(0, 0)
    _collidables: CollidablesStorage = CollidablesStorage()
    _player: Player

    def __init__(self, level_size: Size2D = (1920, 1080)):
        self._size = level_size

        # FIXME: temporary background
        tile_img = image.load(
            Path(__file__).parent / "../assets/images/trash/tile.png"
        ).convert_alpha()
        self.tile_img = scale_pixel_image(tile_img)

        with open(Path(__file__).parent / "../assets/maps/trash_map.txt") as f:
            self.map_array = [[int(x) for x in line.split()] for line in f.readlines()]

    # generates the structure of the level, different params could be passed in the future
    def generate(self):
        self._floor = CollisionSurface(SurfaceType.VERTICAL, self._size[0], self._size[1])
        self._floor.add_breakpoints([(0, 180)])
        self._floor.lock()

    # creates new player on the level (could be used in reset)
    def spawn_player(self, pos: Point = (0, 181)):
        self._player = Player(pos)
        self._collidables.extend([self._player])
        self._camera.bind_player(self._player)

    def reset(self):
        pass

    # will be called in the main event loop
    def update(self, display: Surface, motion_vector: Vector2D):
        display.fill('grey')

        # background tiles
        tile_size = get_scaled_size((32, 32))
        for i, row in enumerate(self.map_array):
            for j, item in enumerate(row):
                if item:
                    tile = self.tile_img.get_rect().move(
                        *self._camera.calc_render_coords(
                            BaseEntity(
                                x=i * tile_size[0] + 400, y=j * tile_size[1] - 500,
                                width=32, height=32
                            ))
                    )
                    display.blit(self.tile_img, tile)

        self._player.update(display, motion_vector, self._camera.calc_render_coords(self._player))
        # FIXME: add proper collision checking
        if True:
            self._player.move(motion_vector)
        self._camera.move(motion_vector)




