import sys
import time
from itertools import chain

import pygame
import logging

from the_hammer_lord.persons.enemy import BaseEnemy
from the_hammer_lord.settings import *

from the_hammer_lord.persons.player import Player
from the_hammer_lord.utils.camera import (
    get_scaled_size,
    scale_pixel_image,
)

from the_hammer_lord.settings import camera, ObjectsStorage


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
    screen = pygame.display.set_mode(SCREEN_SIZE, vsync=True)
    frame_cap = 1.0 / 120
    time_1 = time.perf_counter()
    unprocessed = 0

    # clock = pygame.time.Clock() <- an alternative to perf_counter

    player = Player()
    camera.introduce_player(player)

    enemies = [
        BaseEnemy(500, 1000, target_for_chasing=player),
        BaseEnemy(800, 1500, target_for_chasing=player),
    ]

    objectsStorage.extend(chain((player,), enemies))

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
            for enemy in enemies:
                enemy.main(display=screen)
            pygame.display.flip()