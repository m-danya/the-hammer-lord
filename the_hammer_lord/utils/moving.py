from the_hammer_lord.types import Point, Vector2D


def move_to_target_1d(
    target_coordinate: int,
    current_coordinate: int,
    max_speed: int,
    *,
    camera_mode: bool = False,
):
    # slowly move closer to the target
    difference = target_coordinate - current_coordinate
    if abs(difference) > 1:  # if target is too far
        sign = 1 if difference > 0 else -1
        # move towards the target not faster than max_speed
        if camera_mode:
            speed = int(abs(difference) * max_speed)
            min_speed = min(1, abs(difference))
            return current_coordinate + sign * max(speed, min_speed)
        else:
            return current_coordinate + sign * min(abs(difference), max_speed)
    return target_coordinate


def move_to_target_2d(target: Point, current: Point, max_speed: int):
    return (
        move_to_target_1d(target[0], current[0], max_speed),
        move_to_target_1d(target[1], current[1], max_speed),
    )
