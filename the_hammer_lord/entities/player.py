from math import floor

import pygame.key
from pygame import time, image, transform, Surface
from pygame.sprite import Group, Sprite

from the_hammer_lord.entities.base import Entity
from the_hammer_lord.level.collision_surface import CollisionSurface
from the_hammer_lord.types import Vector2D, PlayerAction, Point
from the_hammer_lord.settings import *
from the_hammer_lord.assets.sprites import PLAYER_ANIMATIONS
from the_hammer_lord.ui.health_bar import HealthBar
from the_hammer_lord.utils.collidables_storage import CollidablesStorage


class Player(Entity):
    _animations: dict[PlayerAction, list[Surface]]
    _current_frame: int = 0
    _current_action: PlayerAction = PlayerAction.IDLE
    _health_bar: HealthBar
    _update_time: int = time.get_ticks()
    _vx: float = 0
    _vy: float = 0
    _is_on_land: bool = False

    def __init__(self, position: Point = (0, 0)):
        super().__init__(
            dimensions=(
                PLAYER_SPRITE_WIDTH * SCALE_RATIO,
                PLAYER_SPRITE_HEIGHT * SCALE_RATIO,
            ),
            position=position,
        )
        # load player animations
        self._load_animations()
        self.image = self._animations[self._current_action][self._current_frame]
        self._health_bar = HealthBar(PLAYER_HEALTH)

    @property
    def is_on_land(self):
        return self._is_on_land

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

    def update(self, display: Surface, render_pos: Point):
        self.render(display, render_pos)
        self._animation_step()

    def render(self, display: Surface, pos: Point):
        display.blit(
            self.image,
            pos,
        )
        # render health bar
        self._health_bar.render(
            display,
            (pos[0] + 45, pos[1] - 15),
        )

    def move(self, ctrls_vector: Vector2D, collidablesStorage: CollidablesStorage):
        # TODO: move collision logic to Entity OR to CollidablesStorage
        self._vx = ctrls_vector[0]
        self.rect.x += self._vx
        sprites = []
        for collidables in collidablesStorage.objects:
            if isinstance(collidables, CollisionSurface):
                sprites.extend(collidables.get_sprites())
            elif isinstance(collidables, Group):
                sprites.extend(collidables)
            elif isinstance(collidables, Sprite):
                sprites.append(collidables)
            else:
                raise NotImplementedError
        collided_surfaces_by_x = pygame.sprite.spritecollide(self, sprites, False)
        for collided_surface in collided_surfaces_by_x:
            if self._vx > 0:
                self.rect.right = collided_surface.rect.left
                self._vx = 0
            elif self._vx < 0:
                self.rect.left = collided_surface.rect.right
                self._vx = 0

        if not self._is_on_land:
            # you can't jump if you're in the air
            ctrls_vector[1] = 0
            self._vy += GRAVITY_FORCE
        self._vy += ctrls_vector[1]
        self._vy += MAGIC_COLLISION_SHIFT  # avoid weird shaking
        self.rect.y += self._vy
        collided_surfaces_by_y = pygame.sprite.spritecollide(
            self, collidablesStorage.objects[0].get_sprites(), False
        )

        self._is_on_land = False
        for collided_surface in collided_surfaces_by_y:
            if self._vy > 0:
                self.rect.bottom = collided_surface.rect.top
                self._vy = 0
                self._is_on_land = True
            else:
                self.rect.top = collided_surface.rect.bottom
                self._vy = 0
