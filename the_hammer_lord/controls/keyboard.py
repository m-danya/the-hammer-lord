import pygame

from the_hammer_lord.controls.controls import IControls


class KeyboardControls(IControls):
    def _get_input(self):
        keys = pygame.key.get_pressed()
        l_pressed = keys[pygame.K_a]
        r_pressed = keys[pygame.K_d]
        sp_pressed = keys[pygame.K_SPACE]

        if l_pressed and not r_pressed:
            self._motion_vector[0] = -0.5
        elif r_pressed and not l_pressed:
            self._motion_vector[0] = 0.5
        else:
            self.motion_vector[0] = 0

        self._motion_vector[1] = -0.5 if sp_pressed else 0

    def get_input(self, *args, **kwargs):
        self._get_input()
