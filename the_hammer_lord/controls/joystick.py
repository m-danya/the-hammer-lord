from .controls import Controls


class JoystickControls(Controls):
    def _handle_movement(self, axis: int, val: float):
        if axis < 2:
            self.motion_vector[axis] = val
            if abs(self.motion_vector[0]) < 0.1:
                self.motion_vector[0] = 0
            if abs(self.motion_vector[1]) < 0.1:
                self.motion_vector[1] = 0

    def handle_movement(self, *args, **kwargs):
        self._handle_movement(*args, **kwargs)
