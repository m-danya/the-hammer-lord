from math import floor

import pygame
from pygame import Surface
from pygame.color import Color

from the_hammer_lord.types import Size2D, Point
from the_hammer_lord.entities.base import Entity
from the_hammer_lord.utils.camera import Camera
from the_hammer_lord.lightning.consts import ProgressionType, ALPHA_OPAQUE
from the_hammer_lord.lightning.light_source import LightSource


class LightMap:
    _size: Size2D
    _light_sources: list[LightSource]
    _main_fill: Surface

    def __init__(self, size: Size2D):
        self._size = size
        self._light_sources = []
        self._set_main_fill()

    def _set_main_fill(self):
        self._main_fill = Surface(self._size, pygame.SRCALPHA)
        self._main_fill.fill("black")
        self._main_fill.set_alpha(floor(ALPHA_OPAQUE * 0.23))

    def add_light_source(
        self,
        position: Point,
        base_color: Color,
        spread: int = 200,
        opacity_progression: ProgressionType = ProgressionType.LINEAR,
        waver: bool = True,
        bound_to: Entity = None,
    ):
        self._light_sources.append(
            LightSource(position, spread, base_color, opacity_progression, waver, bound_to)
        )

    # tlc - top left corner
    def apply(self, display: Surface, camera_ref: Camera, tlc_pos: Point = (0, 0)):
        cur_map = self._main_fill.copy()
        for light_source in self._light_sources:
            source_pos = camera_ref.calc_render_coords(light_source.rect.topleft)
            light_source.render(
                cur_map,
                source_pos,
            )
            light_source.render_sprite(display, source_pos)
        display.blit(cur_map, tlc_pos, special_flags=pygame.BLEND_RGBA_MULT)
