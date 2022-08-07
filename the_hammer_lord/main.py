import sys
import time
import pygame
from pathlib import Path
import logging

from .settings import *

from .player import Player
from .camera import (
    Camera,
    get_scaled_size,
    scale_pixel_image,
)

from .settings import camera


def main():
    # prepare a joystick
    joystick_motion = [0, 0]
    try:
        pygame.joystick.init()
        joystick = pygame.joystick.Joystick(0)
    except pygame.error:
        logging.error(
            "Insert a controller to play this game, there is no keyboard"
            " support for now :("
        )
        exit(1)

    # prepare to draw
    pygame.init()
    pygame.display.set_caption("The Hammer Lord")
    screen = pygame.display.set_mode(SCREEN_SIZE)
    frame_cap = 1.0 / 120
    time_1 = time.perf_counter()
    unprocessed = 0

    # clock = pygame.time.Clock() <- an alternative to perf_counter

    player = Player()

    # some graphic objects
    # (they will be removed when the level system will be implemented)
    tile_img = pygame.image.load(
        Path(__file__).parent / "assets/images/trash/tile.png"
    ).convert_alpha()
    tile_img = scale_pixel_image(tile_img)

    k_img = pygame.image.load(
        Path(__file__).parent / "assets/images/trash/k.png"
    ).convert_alpha()
    k_img = scale_pixel_image(k_img)

    with open(Path(__file__).parent / "assets/maps/trash_map.txt") as f:
        map_array = [[int(x) for x in line.split()] for line in f.readlines()]

    while True:
        can_render = False
        time_2 = time.perf_counter()
        passed = time_2 - time_1
        unprocessed += passed
        time_1 = time_2
        while unprocessed >= frame_cap:
            unprocessed -= frame_cap
            can_render = True
        if can_render:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis < 2:
                        joystick_motion[event.axis] = event.value
                        if abs(joystick_motion[0]) < 0.1:
                            joystick_motion[0] = 0
                        if abs(joystick_motion[1]) < 0.1:
                            joystick_motion[1] = 0
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    pygame.quit()
                    sys.exit()

            screen.fill("grey")

            # background tiles
            tile_size = get_scaled_size((32, 32))
            for i, row in enumerate(map_array):
                for j, item in enumerate(row):
                    if item:
                        tile = tile_img.get_rect().move(
                            *camera.get_object_coords(
                                i * tile_size[0] + 400, j * tile_size[1] - 500
                            )
                        )
                        screen.blit(tile_img, tile)

            # superkontik, will be removed (isn't it?)
            k_rect = k_img.get_rect()
            k_rect = k_rect.move(*camera.get_object_coords(2400, 1500))
            screen.blit(k_img, k_rect)

            # draw properly implemented objects
            camera.main(joystick_motion=joystick_motion)
            player.main(display=screen, joystick_motion=joystick_motion)

            pygame.display.flip()
