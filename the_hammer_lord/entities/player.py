from pygame import time, image, transform, Surface, Rect
from pygame.sprite import Sprite

from the_hammer_lord.types import Vector2D, PlayerAction, Point
from the_hammer_lord.entities.base import DynamicEntity
from the_hammer_lord.settings import *
from the_hammer_lord.assets.sprites import PLAYER_ANIMATIONS
from the_hammer_lord.ui.health_bar import HealthBar
from the_hammer_lord.global_ctx import collidablesStorage


class Player(DynamicEntity):
    _animations: dict[PlayerAction, list[Surface]] = {}
    _current_frame: int = 0
    _current_action: PlayerAction = PlayerAction.IDLE
    _health_bar: HealthBar = HealthBar(PLAYER_HEALTH)
    _update_time: int = time.get_ticks()

    def __init__(self, pos: Point = (PLAYER_COORDS_CENTERED[0], PLAYER_COORDS_CENTERED[1])):
        super().__init__(dimensions=(PLAYER_SPRITE_WIDTH * SCALE_RATIO, PLAYER_SPRITE_HEIGHT * SCALE_RATIO), pos=pos)
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

    def _animation_step(self):
        # check if enough time has passed since the last update
        if time.get_ticks() - self._update_time > PLAYER_ANIMATION_COOLDOWN:
            self._current_frame += 1
            self._current_frame %= PLAYER_ANIMATIONS[self._current_action].frames_cnt
            self._update_time = time.get_ticks()
            # update image
            self.image = self._animations[self._current_action][self._current_frame]

    def update(self, display: Surface, motion_vector: Vector2D, render_pos: Point):
        self.render(display, render_pos)
        self._animation_step()

    def render(self, display: Surface, pos: Point):
        # render player model
        display.blit(
            self.image,
            pos,
        )

        # render health bar
        self._health_bar.render(
            display,
            (pos[0] - 15, pos[1] - self.rect.height // 2 + 15),
        )

    def move(self, motion_vector: Vector2D):
        # FIXME: add appropriate vertical collision tracking
        if self.y > 1500:
            self.y = 1500
            motion_vector[1] = 0

        # top left corner coords are recalculated automatically
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.x += motion_vector[0] * CAMERA_SPEED
        self.y += motion_vector[1] * CAMERA_SPEED
