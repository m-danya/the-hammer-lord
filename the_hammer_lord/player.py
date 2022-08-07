import pygame

from .settings import *


class Player:
    def __init__(self):
        self.scaled_size = (
            PLAYER_SPRITE_WIDTH * SCALE_RATIO,
            PLAYER_SPRITE_HEIGHT * SCALE_RATIO,
        )
        self.x = (
            SCREEN_SIZE[0] - self.scaled_size[0]
        ) / 2 + PLAYER_SHIFT_FROM_CENTER_X
        self.y = (
            SCREEN_SIZE[1] - self.scaled_size[1]
        ) / 2 + PLAYER_SHIFT_FROM_CENTER_Y
        self.animations_length = {PlayerAction.IDLE: 3}
        self.images = self.load_images()
        self.action = PlayerAction.IDLE
        self.frame_index = 0
        self.image = self.images[self.action][self.frame_index]

        self.update_time = pygame.time.get_ticks()

    def main(self, display: pygame.Surface, joystick_motion):
        self.move(joystick_motion)
        display.blit(
            self.image,
            camera.get_object_coords(self.x, self.y),
        )
        animation_cooldown = 350
        # update image
        self.image = self.images[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            if self.frame_index >= self.animations_length[self.action]:
                self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def move(self, joystick_motion):
        self.x += joystick_motion[0] * CAMERA_SPEED
        self.y += joystick_motion[1] * CAMERA_SPEED

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
                        self.scaled_size,
                    )
                )
            animation_list[action] = temp_img_list
        return animation_list
