from objects.motion.motion import Motion


class BaseDirectionalGenerator:
    def __init__(self, motion: Motion):
        self.motion = motion
        self.other_motion = motion.pictograph.get.other_motion(motion)

    def generate_directional_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        raise NotImplementedError("Subclasses must implement this method.")
