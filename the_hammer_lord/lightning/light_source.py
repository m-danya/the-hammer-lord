import math

import pygame
from pygame import Surface, draw
from pygame.color import Color

from the_hammer_lord.types import Point
from the_hammer_lord.entities.base import Entity
from the_hammer_lord.utils.colors import linear_color_alpha_fade
from the_hammer_lord.utils.transform import load_scaled_image
from the_hammer_lord.lightning.consts import (
    TORCH_DIMENSIONS,
    ProgressionType,
)

WAVER_FRAME_BUFFER = 3


# TODO: separate radial / directional light
class LightSource(Entity):
    _emission_spread: int
    _opacity_progression: ProgressionType
    _wavering: bool
    _wavering_degree: int = 3
    _base_color: Color
    _emission: Surface
    _dynamic: bool
    _cur_layers_cnt: int = 0
    _fade_in: bool = False
    _buffered_frames_cnt: int = 0

    def __init__(
        self,
        position: Point,
        spread: int,
        base_color: Color,
        opacity_progression: ProgressionType,
        waver: bool,
        bound_to: Entity,
        # TODO: get image from sprite
        sprite: Surface = None,
    ):
        super().__init__(dimensions=TORCH_DIMENSIONS, position=position)
        self.image = load_scaled_image("Torch", TORCH_DIMENSIONS)
        self._emission_spread = spread
        self._base_color = base_color
        self._opacity_progression = opacity_progression
        self._wavering = waver
        # used for dynamic light positioning, e.g. allows for glow to move around with player
        self._dynamic = bound_to is not None
        if self._dynamic:
            self.rect = bound_to.rect
            self.image = None

    def _calc_wavering_level(self, target_layer_cnt: int) -> int:
        if not self._wavering:
            return target_layer_cnt

        if self._cur_layers_cnt <= 0:
            self._cur_layers_cnt = target_layer_cnt

        if self._buffered_frames_cnt != 0:
            return self._cur_layers_cnt

        if self._cur_layers_cnt == target_layer_cnt - self._wavering_degree:
            self._fade_in = False
        elif self._cur_layers_cnt == target_layer_cnt + self._wavering_degree:
            self._fade_in = True

        self._cur_layers_cnt += -1 if self._fade_in else 1
        return self._cur_layers_cnt

    # TODO: make abstract?
    def _form_linear_emission(
        self,
        layer_cnt: int = 10,
    ):
        self._emission = Surface(
            (self._emission_spread * 2, self._emission_spread * 2), flags=pygame.SRCALPHA
        )
        layer_cnt = self._calc_wavering_level(layer_cnt)
        layer_width = self._emission_spread // layer_cnt
        emission_center = self._emission.get_rect().center
        core_layer_width = math.floor(1.5 * layer_width)
        for cur_layer_ind in range(layer_cnt):
            cur_layer = linear_color_alpha_fade(self._base_color, cur_layer_ind / layer_cnt)
            cur_layer_width = (
                self._emission_spread - layer_width * cur_layer_ind
                if cur_layer_ind != layer_cnt - 1
                else core_layer_width
            )
            draw.circle(
                self._emission,
                color=cur_layer,
                center=emission_center,
                radius=cur_layer_width,
            )

    # renders emission on the lightmap
    def render(self, lightmap: Surface, pos: Point):
        self._buffered_frames_cnt += 1
        self._buffered_frames_cnt %= WAVER_FRAME_BUFFER
        match self._opacity_progression:
            case ProgressionType.LINEAR:
                self._form_linear_emission()
            case _:
                raise RuntimeError("unsupported opacity progression type")

        adjusted_pos = (
            pos
            if not self._dynamic
            else (pos[0] - self.rect.width // 4, pos[1] - self.rect.height // 4)
        )
        lightmap.blit(self._emission, adjusted_pos)

    # renders light source sprite over the emission
    def render_sprite(self, display: Surface, pos: Point):
        if self.image is None:
            return

        adjusted_pos = (
            pos[0] + self._emission.get_width() // 2 - self.image.get_width() // 2,
            pos[1] + self._emission.get_height() // 2 - self.image.get_height() // 2,
        )
        display.blit(self.image, adjusted_pos)
