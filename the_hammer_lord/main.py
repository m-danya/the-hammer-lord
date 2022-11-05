import time
import logging
import sys

import pygame

from the_hammer_lord.settings import SCREEN_SIZE, TARGET_FRAMERATE
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
    ticker = pygame.time.Clock()

    current_level = Level()
    current_level.setup()

    # using ns for better precision
    prev_time = time.perf_counter_ns()

    # main event loop
    while True:
        cur_time = time.perf_counter_ns()
        # TODO: should be used to neglect animation speeds difference on an arbitrary framerate
        dt = (cur_time - prev_time) / 1e9
        prev_time = cur_time

        for event in pygame.event.get():
            match event.type:
                case pygame.JOYAXISMOTION:
                    move_controls.get_input(event.axis, event.value)
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit_game()
                case pygame.QUIT:
                    exit_game()

        if isinstance(move_controls, KeyboardControls):
            move_controls.get_input()

        # render current level
        current_level.update(display=screen, motion_vector=move_controls.motion_vector)
        pygame.display.flip()

        ticker.tick(TARGET_FRAMERATE)
