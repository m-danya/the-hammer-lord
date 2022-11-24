from pygame import Surface, image, time

from the_hammer_lord.assets.sprites import SPRITES
from the_hammer_lord.entities.base import Entity
from the_hammer_lord.settings import (
    MAGIC_COLLISION_SHIFT,
    PLATFORM_SPEED,
    PLATFORM_TIMEOUT,
)
from the_hammer_lord.utils.camera import Camera
from the_hammer_lord.utils.collidables_storage import CollidablesStorage
from the_hammer_lord.utils.moving import move_to_target_2d
from the_hammer_lord.utils.transform import fill_surface


class Platform(Entity):
    def __init__(self, width, height, states):
        super().__init__(
            dimensions=(
                width,
                height,
            ),
            position=(
                # first available (x, y)
                next(
                    (state[0], state[1])
                    for state in states
                    if isinstance(state, tuple)
                )
            ),
        )
        self._texture = image.load(SPRITES["BrickTile2"]).convert_alpha()
        self.image = fill_surface(
            (self.rect.width, self.rect.height), self._texture
        )

        # TODO: replace with enum / classes for actions
        self._states = states
        self._state_idx = 0
        self._is_sleeping = False
        self._sleep_started_time = None

    def move(self, collidable_creatures: CollidablesStorage):
        match self._states[self._state_idx]:
            case (target_x, target_y):
                new_x, new_y = move_to_target_2d(
                    (target_x, target_y),
                    (self.rect.x, self.rect.y),
                    PLATFORM_SPEED,
                )
                if (new_x, new_y) == (self.rect.x, self.rect.y):
                    self._state_idx = (self._state_idx + 1) % len(self._states)
                else:
                    # moving logic: throw away all creatures that collides with me
                    vx = new_x - self.rect.x
                    self.rect.x += vx
                    npcs_collided_by_x = (
                        collidable_creatures.get_collided_sprites_with(self)
                    )
                    for collided_npc in npcs_collided_by_x:
                        if vx > 0:
                            collided_npc.rect.left = (
                                self.rect.right + MAGIC_COLLISION_SHIFT
                            )
                        else:
                            collided_npc.rect.right = (
                                self.rect.left - MAGIC_COLLISION_SHIFT
                            )
                        break
                    vy = new_y - self.rect.y
                    self.rect.y += vy
                    npcs_collided_by_y = (
                        collidable_creatures.get_collided_sprites_with(self)
                    )
                    for collided_npc in npcs_collided_by_y:
                        if vy > 0:
                            collided_npc.rect.top = (
                                self.rect.bottom + MAGIC_COLLISION_SHIFT
                            )
                        else:
                            collided_npc.rect.bottom = (
                                self.rect.top - MAGIC_COLLISION_SHIFT
                            )
                        break

            case "sleep":
                if not self._is_sleeping:
                    self._is_sleeping = True
                    self._sleep_started_time = time.get_ticks()
                elif (
                    time.get_ticks() - self._sleep_started_time
                    > PLATFORM_TIMEOUT
                ):
                    self._is_sleeping = False
                    self._state_idx = (self._state_idx + 1) % len(self._states)

    def render(self, display: Surface, camera: Camera):
        display.blit(
            self.image,
            camera.calc_render_coords((self.rect.x, self.rect.y)),
        )
