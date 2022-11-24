import pygame
from pygame import Surface


class DebugInfoCorner:
    """Shows a lot of useful debug information"""

    def __init__(self, level):
        self.level = level
        self.enabled = True
        self._font = pygame.font.Font(None, 42)

    def update(self, display: Surface):
        if not self.enabled:
            return
        debug_data = self._collect_debug_data()
        for i, info_type in enumerate(debug_data):
            text = self._font.render(
                f"{info_type}:{debug_data[info_type]}",
                True,
                (255, 255, 255),
                (0, 0, 0),
            )
            display.blit(text, text.get_rect(x=10, y=10 + i * 35))

    def _collect_debug_data(self):
        return {
            "camera.x": self.level._camera.x,
            "camera.y": self.level._camera.y,
            "player.x": self.level._player.rect.x,
            "player.y": self.level._player.rect.y,
            "player._is_on_the_ground": self.level._player._is_on_the_ground,
            "mouse.x": pygame.mouse.get_pos()[0] + self.level._camera.x,
            "mouse.y": pygame.mouse.get_pos()[1] + self.level._camera.y,
            "lock_x": self.level._camera._lock_x,
            "lock_y": self.level._camera._lock_y,
            "platform_state_idx": self.level._platforms[0]._state_idx,
        }
