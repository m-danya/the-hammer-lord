from typing import Dict, List

from pygame import time, image, transform, Surface, Rect
from pygame.sprite import Sprite

from the_hammer_lord.types import Vector2D, PlayerAction

from the_hammer_lord.settings import *
from the_hammer_lord.assets.sprites import PLAYER_ANIMATIONS
from the_hammer_lord.ui.health_bar import HealthBar
from the_hammer_lord.global_ctx import camera, collidablesStorage


class Player(Sprite):
    x: int = PLAYER_COORDS_CENTERED[0]
    y: int = PLAYER_COORDS_CENTERED[1]
    _animations: Dict[PlayerAction, List[Surface]] = {}
    _current_frame: int = 0
    _current_action: PlayerAction = PlayerAction.IDLE
    _health_bar: HealthBar = HealthBar(PLAYER_HEALTH)
    _update_time: int = time.get_ticks()

    def __init__(self):
        super().__init__()

        # assign associated rectangle
        self.rect = Rect((self.x, self.y), (PLAYER_SPRITE_WIDTH * SCALE_RATIO, PLAYER_SPRITE_HEIGHT * SCALE_RATIO))

        # load player animations
        self._load_animations()
        self.image = self._animations[self._current_action][self._current_frame]

    def _load_animations(self):
        for action in PlayerAction:
            # 1. load sprite containing animation frames
            sprite = image.load(PLAYER_ANIMATIONS[action].sprite_path).convert_alpha()

            # 2. extract each frame from it
            self._animations[action] = []
            for x in range(PLAYER_ANIMATIONS[action].frames_cnt):
                animation_frame = sprite.subsurface(
                    x * PLAYER_SPRITE_WIDTH,
                    0,  # cause there is only one row
                    PLAYER_SPRITE_WIDTH,
                    PLAYER_SPRITE_HEIGHT,
                )

                self._animations[action].append(
                    transform.scale(
                        animation_frame,
                        (self.rect.width, self.rect.height),
                    )
                )

    @property
    def camera_adjusted_coords(self) -> Vector2D:
        return self.x - PLAYER_COORDS_CENTERED[0], self.y - PLAYER_COORDS_CENTERED[1]

    def main(self, display: Surface, motion_vector: Vector2D):
        self.move(motion_vector)
        self.render(display)
        self.animation_step()

    def animation_step(self):
        # check if enough time has passed since the last update
        if time.get_ticks() - self._update_time > PLAYER_ANIMATION_COOLDOWN:
            self._current_frame += 1
            self._current_frame %= PLAYER_ANIMATIONS[self._current_action].frames_cnt
            self._update_time = time.get_ticks()
            # update image
            self.image = self._animations[self._current_action][self._current_frame]

    def render(self, display):
        # render player model
        display.blit(
            self.image,
            camera.get_object_coords(
                self.x - self.rect.width // 2,
                self.y - self.rect.height // 2,
            ),
        )

        # render health bar
        self._health_bar.render(
            display,
            self.x - 15,
            self.y - self.rect.height // 2 + 15,
        )

    def move(self, motion_vector: Vector2D):
        # FIXME: add appropriate vertical collision tracking
        if self.y > 1500:
            self.y = 1500
            motion_vector[1] = 0

        dx = motion_vector[0] * CAMERA_SPEED
        dy = motion_vector[1] * CAMERA_SPEED

        # update rectangle's top left corner coords
        # according to the player's current position
        # FIXME: may be unnecessary now, but have to be updated
        # self.rect.left = self.x - self.rect.width // 2
        # self.rect.top = self.y - self.rect.height // 2
        # top left corner coords are recalculated automatically
        self.rect.centerx = self.x
        self.rect.centery = self.y
        if collidablesStorage.can_move(self.rect, dx, dy):
            self.x += dx
            self.y += dy
