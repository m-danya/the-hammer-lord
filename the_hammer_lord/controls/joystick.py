from the_hammer_lord.controls.controls import IControls


class JoystickControls(IControls):
    def _handle_movement(self, axis: int, val: float):
        # TODO: apply constants from settings here to get
        #  the same speed as with keyboard controls
        raise NotImplementedError
        if axis < 2:
            self._motion_vector[axis] = val
            if abs(self._motion_vector[0]) < 0.1:
                self._motion_vector[0] = 0
            if abs(self._motion_vector[1]) < 0.1:
                self._motion_vector[1] = 0

    def get_input(self, *args, **kwargs):
        self._handle_movement(*args, **kwargs)
