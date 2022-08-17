import enum
from pathlib import Path


SCREEN_SIZE = 1366, 768
SCALE_RATIO = 4
CAMERA_SPEED = 4
PLAYER_SPRITE_WIDTH = 80
PLAYER_SPRITE_HEIGHT = 64
PLAYER_SHIFT_FROM_CENTER_X = 70  # to center the player without hammer
PLAYER_SHIFT_FROM_CENTER_Y = 0
PLAYER_ANIMATION_COOLDOWN = 350

ENEMY_TEST_RECT_SIZE = 100, 150
ENEMY_SPEED = 2


ENEMY_HEALTH = 100
PLAYER_HEALTH = 300

HEALTH_BAR_THICKNESS = 3


class PlayerAction(enum.Enum):
    IDLE = enum.auto()


SPRITE_PATHS = {
    PlayerAction.IDLE: Path(__file__).parent / "assets/images/main_idle.png"
}

from the_hammer_lord.utils.objects_storage import ObjectsStorage

objectsStorage = ObjectsStorage()

from the_hammer_lord.utils.camera import Camera

camera = Camera(0, 0)
