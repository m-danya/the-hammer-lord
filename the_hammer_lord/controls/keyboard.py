import pygame
from .controls import Controls


class KeyboardControls(Controls):
    _jumping: bool = False

    def _handle_movement(self, key: pygame.key, key_up: bool = False):
        match key:
            case pygame.K_a:
                self.motion_vector[0] = -0.5 if not key_up else 0
            # right movement
            case pygame.K_d:
                self.motion_vector[0] = 0.5 if not key_up else 0
            # jumping
            case pygame.K_SPACE:
                # confirm the character is standing on the ground
                if not self._jumping:
                    self.motion_vector[1] = -0.5

    def handle_movement(self, *args, **kwargs):
        self._handle_movement(*args, **kwargs)
