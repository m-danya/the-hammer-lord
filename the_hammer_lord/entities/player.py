from math import floor

import pygame.key
from pygame import time, image, transform, Surface

from the_hammer_lord.types import Vector2D, PlayerAction, Point
from the_hammer_lord.entities.base import DynamicEntity
from the_hammer_lord.settings import *
from the_hammer_lord.assets.sprites import PLAYER_ANIMATIONS
from the_hammer_lord.ui.health_bar import HealthBar


class Player(DynamicEntity):
    _animations: dict[PlayerAction, list[Surface]]
    _current_frame: int = 0
    _current_action: PlayerAction = PlayerAction.IDLE
    _health_bar: HealthBar
    _update_time: int = time.get_ticks()
    _in_air: bool = False
    _motion_vector: Vector2D

    def __init__(self, pos: Point = (0, 0)):
        super().__init__(
            dimensions=(
                PLAYER_SPRITE_WIDTH * SCALE_RATIO,
                PLAYER_SPRITE_HEIGHT * SCALE_RATIO,
            ),
            pos=pos,
        )
        # load player animations
        self._load_animations()
        self.image = self._animations[self._current_action][self._current_frame]
        self._health_bar = HealthBar(PLAYER_HEALTH)
        self._motion_vector = [0, 0]

    def _load_animations(self):
        self._animations = {}
        for action in PlayerAction:
            # 1. load sprite containing animation frames
            sprite = image.load(PLAYER_ANIMATIONS[action].sprite_path).convert_alpha()

            # TODO: move to logic to a separate util function
            #  since we will be using it in other classes as well
            # 2. extract each frame from it
            self._animations[action] = []
            for frame_idx in range(PLAYER_ANIMATIONS[action].frames_cnt):
                animation_frame = sprite.subsurface(
                    frame_idx * PLAYER_SPRITE_WIDTH,
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
            # update player's animation frame
            self.image = self._animations[self._current_action][self._current_frame]

    def _apply_gravity(self):
        self._motion_vector[1] += GRAVITY_FORCE

    def update(self, display: Surface, render_pos: Point):
        self.render(display, render_pos)
        self._animation_step()

    def render(self, display: Surface, pos: Point):
        shifted_pos = (pos[0] - self.rect.width // 2, pos[1] - self.rect.height // 2)
        # render player model
        display.blit(
            self.image,
            shifted_pos,
        )

        # render health bar
        self._health_bar.render(
            display,
            (shifted_pos[0] + 45, shifted_pos[1] - 15),
        )

    def in_air(self):
        return self._in_air

    def move(self, ctrls_vector: Vector2D, land: bool = False):
        if land:
            self._motion_vector[1] = 0
            self._in_air = False
        else:
            self._apply_gravity()

        if ctrls_vector[1] != 0 and not self._in_air:
            self._in_air = True
            self._motion_vector[1] = ctrls_vector[1]

        self._motion_vector[0] = ctrls_vector[0]

        self.x += floor(self._motion_vector[0] * CAMERA_SPEED)
        self.y += floor(self._motion_vector[1] * CAMERA_SPEED)
        self.rect.left = self.x
        self.rect.top = self.y
