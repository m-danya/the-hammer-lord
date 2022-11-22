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
    "LevelBackground1": (f"{Path(__file__).parent}/images/backgrounds/level_background1.jpg"),
    "LevelBackground2": (f"{Path(__file__).parent}/images/backgrounds/level_background2.png"),
    "BrickTile": f"{Path(__file__).parent}/images/tiles/brick_tile_painted.jpg",
    "Torch": f"{Path(__file__).parent}/images/interior/torch.png",
    "RadialLight": f"{Path(__file__).parent}/images/effects/radial_light.png",
}
