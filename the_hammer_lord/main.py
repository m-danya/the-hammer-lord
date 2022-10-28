import sys
import time
from itertools import chain

import pygame
import logging

from the_hammer_lord.settings import *

from the_hammer_lord.controls.joystick import JoystickControls
from the_hammer_lord.controls.keyboard import KeyboardControls

from the_hammer_lord.entities.enemy import BaseEnemy
from the_hammer_lord.entities.player import Player

from the_hammer_lord.utils.camera import (
    get_scaled_size,
    scale_pixel_image,
)

from the_hammer_lord.global_ctx import camera, collidablesStorage


def exit_game():
    pygame.quit()
    sys.exit()


def main():
    # TODO: encapsulate in Player class
    move_controls = KeyboardControls()
    # prepare joystick input if available
    try:
        pygame.joystick.init()
        pygame.joystick.Joystick(0)
        move_controls = JoystickControls()
    except pygame.error:
        logging.error("No controller detected, falling back to keyboard insert")

    # prepare to draw
    pygame.init()
    pygame.display.set_caption("The Hammer Lord")
    screen = pygame.display.set_mode(SCREEN_SIZE, vsync=True)
    frame_cap = 1.0 / 120
    time_1 = time.perf_counter()
    unprocessed = 0

    # clock = pygame.time.Clock() <- an alternative to perf_counter

    player = Player()
    camera.bind_player(player)

    enemies = [
        BaseEnemy(500, 1000, target_for_chasing=player),
        BaseEnemy(800, 1500, target_for_chasing=player),
    ]

    collidablesStorage.extend(chain((player,), enemies))

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
                match event.type:
                    case pygame.JOYAXISMOTION:
                        move_controls.handle_movement(event.axis, event.value)
                    case pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            exit_game()

                        move_controls.handle_movement(event.key)
                    case pygame.KEYUP:
                        move_controls.handle_movement(event.key, key_up=True)
                    case pygame.QUIT:
                        exit_game()

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
            # as camera follows our player, we're moving it first
            player.main(display=screen, motion_vector=move_controls.motion_vector)
            camera.main(motion_vector=move_controls.motion_vector)

            # enemy rendering
            for enemy in enemies:
                enemy.main(display=screen)

            pygame.display.flip()
