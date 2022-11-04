import time
import logging
import sys

import pygame

from the_hammer_lord.settings import SCREEN_SIZE
from the_hammer_lord.controls.joystick import JoystickControls
from the_hammer_lord.controls.keyboard import KeyboardControls
from the_hammer_lord.level.level import Level


def exit_game():
    pygame.quit()
    sys.exit()


def main():
    # turn on debug mode for the sake of development
    logging.basicConfig(level=logging.DEBUG)
    move_controls = KeyboardControls()
    # prepare joystick input if available
    try:
        pygame.joystick.init()
        pygame.joystick.Joystick(0)
        move_controls = JoystickControls()
    except pygame.error:
        logging.warning("No controller detected, falling back to keyboard input")

    # prepare to draw
    pygame.init()
    pygame.display.set_caption("The Hammer Lord")
    screen = pygame.display.set_mode(SCREEN_SIZE, vsync=True)
    # there are 1e+9 ns in a single s
    frame_cap = int(1e+9) // 240
    # using ns for better precision
    time_1 = time.perf_counter_ns()
    unprocessed = 0

    # clock = pygame.time.Clock() <- an alternative to perf_counter

    current_level = Level()
    current_level.generate()
    current_level.spawn_player()

    # main event loop
    while True:
        can_render = False
        time_2 = time.perf_counter_ns()
        passed = time_2 - time_1
        unprocessed += passed
        time_1 = time_2
        if unprocessed >= frame_cap:
            unprocessed -= (unprocessed // frame_cap) * frame_cap
            can_render = True

        if not can_render:
            continue

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

        # render current level
        current_level.update(display=screen, motion_vector=move_controls.motion_vector)
        pygame.display.flip()
