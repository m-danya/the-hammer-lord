import pygame

from the_hammer_lord.settings import *


class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def main(self, joystick_motion):
        self.move(joystick_motion)

    def move(self, joystick_motion):
        self.x += joystick_motion[0] * CAMERA_SPEED
        self.y += joystick_motion[1] * CAMERA_SPEED

    def get_object_coords(self, x, y):
        return x - self.x, y - self.y


def get_scaled_size(size: tuple[int, int]):
    return size[0] * SCALE_RATIO, size[1] * SCALE_RATIO


def scale_pixel_image(image: pygame.Surface):
    size = image.get_size()
    scaled = pygame.transform.scale(image, get_scaled_size(size))
    return scaled
