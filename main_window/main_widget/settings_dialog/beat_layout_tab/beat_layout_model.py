class BeatLayoutModel:
    def __init__(self, num_beats: int, valid_layouts: list[tuple[int, int]]):
        self.num_beats = num_beats
        self.valid_layouts = valid_layouts
        self.current_layout = valid_layouts[0]
