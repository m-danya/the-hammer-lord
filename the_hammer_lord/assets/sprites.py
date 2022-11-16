from pathlib import Path
from typing import Dict

from the_hammer_lord.types import Animation, PlayerAction


PLAYER_ANIMATIONS: Dict[PlayerAction, Animation] = {
    PlayerAction.IDLE: Animation(
        sprite_path=f"{Path(__file__).parent}/images/main_idle.png",
        frames_cnt=3,
    ),
}

SPRITES = {
    "LevelBackground1": (
        f"{Path(__file__).parent}/images/backgrounds/level_background1.jpg"
    ),
    "BrickTile": f"{Path(__file__).parent}/images/tiles/brick_tile_painted.jpg",
}
