import pygame

from the_hammer_lord.controls.controls import IControls
from the_hammer_lord.settings import (
    PLAYER_JUMPING_MOMENTUM,
    PLAYER_SPEED_HORIZONTAL,
)


class KeyboardControls(IControls):
    def _get_input(self):
        keys = pygame.key.get_pressed()
        l_pressed = keys[pygame.K_a]
        r_pressed = keys[pygame.K_d]
        sp_pressed = keys[pygame.K_SPACE]

        if l_pressed and not r_pressed:
            self._motion_vector[0] = -PLAYER_SPEED_HORIZONTAL
        elif r_pressed and not l_pressed:
            self._motion_vector[0] = PLAYER_SPEED_HORIZONTAL
        else:
            self.motion_vector[0] = 0

        self._motion_vector[1] = -PLAYER_JUMPING_MOMENTUM if sp_pressed else 0

    def get_input(self, *args, **kwargs):
        self._get_input()
