import pygame
from pygame import Surface


class DebugInfoCorner:
    """Shows a lot of useful debug information"""

    def __init__(self, level):
        self.level = level
        self.enabled = True

    def update(self, display: Surface):
        if self.enabled:
            font = pygame.font.Font(None, 42)
            debug_data = {
                "camera.x": self.level._camera.x,
                "camera.y": self.level._camera.y,
                "player.x": self.level._player.rect.x,
                "player.y": self.level._player.rect.y,
                "player._is_on_land": self.level._player._is_on_land,
                "mouse.x": pygame.mouse.get_pos()[0],
                "mouse.y": pygame.mouse.get_pos()[1],
                "lock_x": self.level._camera._lock_x,
                "lock_y": self.level._camera._lock_y,
            }
            for i, info_type in enumerate(debug_data):
                text = font.render(
                    f"{info_type}:{debug_data[info_type]}",
                    True,
                    (255, 255, 255),
                    (0, 0, 0),
                )
                display.blit(text, text.get_rect(x=10, y=10 + i * 35))
