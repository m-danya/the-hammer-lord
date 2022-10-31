import pygame

from the_hammer_lord.types.movement import Vector2D
from the_hammer_lord.entities.base import BaseEntity

from the_hammer_lord.settings import *
from the_hammer_lord.ui.health_bar import HealthBar
from the_hammer_lord.global_ctx import camera, collidablesStorage


class Player(BaseEntity):
    def __init__(self):
        self.width = PLAYER_SPRITE_WIDTH * SCALE_RATIO
        self.height = PLAYER_SPRITE_HEIGHT * SCALE_RATIO
        # center coords
        self.x = PLAYER_COORDS_CENTERED[0]
        self.y = PLAYER_COORDS_CENTERED[1]

        self.animations_length = {PlayerAction.IDLE: 3}
        self.images = self.load_images()
        self.action = PlayerAction.IDLE
        self.frame_index = 0
        self.image = self.images[self.action][self.frame_index]

        self.health_bar = HealthBar(PLAYER_HEALTH)

        self.update_time = pygame.time.get_ticks()

    @property
    def camera_adjusted_coords(self) -> Vector2D:
        return self.x - PLAYER_COORDS_CENTERED[0], self.y - PLAYER_COORDS_CENTERED[1]

    def main(self, display: pygame.Surface, motion_vector: Vector2D):
        self.move(motion_vector)
        self.render(display)
        self.animation_step()

    def animation_step(self):
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > PLAYER_ANIMATION_COOLDOWN:
            self.frame_index += 1
            if self.frame_index >= self.animations_length[self.action]:
                self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            # update image
            self.image = self.images[self.action][self.frame_index]

    def render(self, display):
        # sprite
        display.blit(
            self.image,
            camera.get_object_coords(
                self.x - self.width // 2,
                self.y - self.height // 2,
            ),
        )

        # health bar
        self.health_bar.render(
            display,
            self.x - 15,
            self.y - self.height // 2 + 15,
        )

    def move(self, motion_vector: Vector2D):
        # FIXME: add appropriate vertical collision tracking
        if self.y > 1500:
            self.y = 1500
            motion_vector[1] = 0

        dx = motion_vector[0] * CAMERA_SPEED
        dy = motion_vector[1] * CAMERA_SPEED

        if collidablesStorage.can_move(self, dx, dy):
            self.x += dx
            self.y += dy

    def load_images(self):
        animation_list = {}

        for action in PlayerAction:
            # 1. load an image
            sheet = pygame.image.load(SPRITE_PATHS[action]).convert_alpha()

            # 2. extract the animation from it
            temp_img_list = []
            animation_length = self.animations_length[action]
            for x in range(animation_length):
                temp_img = sheet.subsurface(
                    x * PLAYER_SPRITE_WIDTH,
                    0,  # cause there is only one row
                    PLAYER_SPRITE_WIDTH,
                    PLAYER_SPRITE_HEIGHT,
                )
                temp_img_list.append(
                    pygame.transform.scale(
                        temp_img,
                        (self.width, self.height),
                    )
                )
            animation_list[action] = temp_img_list
        return animation_list
