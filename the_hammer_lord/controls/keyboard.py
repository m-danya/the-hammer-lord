import pygame

from the_hammer_lord.controls.controls import IControls


class KeyboardControls(IControls):
    def _handle_movement(self, key: pygame.key, key_up: bool = False):
        # FIXME: in current implementation key_up param can abruptly interrupt movement
        match key:
            # left movement
            case pygame.K_a:
                self._motion_vector[0] = -0.5 if not key_up else 0
            # right movement
            case pygame.K_d:
                self._motion_vector[0] = 0.5 if not key_up else 0
            # jumping
            case pygame.K_SPACE:
                self._motion_vector[1] = -0.5 if not key_up else 0

    def handle_movement(self, *args, **kwargs):
        self._handle_movement(*args, **kwargs)
