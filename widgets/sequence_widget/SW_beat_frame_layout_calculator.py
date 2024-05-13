from typing import TYPE_CHECKING

from widgets.sequence_widget.SW_beat_frame.beat import BeatView


if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import SW_BeatFrame


class SW_BeatFrameLayoutManager:
    def __init__(self, beat_frame: "SW_BeatFrame"):
        self.beat_frame = beat_frame
        self.selection_manager = beat_frame.selection_manager
        self.beats: list[BeatView] = beat_frame.beats

    def calculate_layout(self, beat_count: int) -> tuple[int, int]:
        layout_options = self.get_layouts()
        return layout_options[beat_count]

    def configure_beat_frame(self, num_beats):
        # Assuming a method that calculates the layout based on num_beats
        columns, rows = self.calculate_layout(num_beats)  # +1 for the start position
        self.rearrange_beats(columns, rows)
        # update the selection overlay
        # selected_beat = self.selection_manager.selected_beat
        # if selected_beat:
        #     self.selection_manager.deselect_beat()
        #     self.selection_manager.select_beat(selected_beat)
        #     self.selection_manager.update_overlay_position()

    def rearrange_beats(self, columns, rows):
        # Clear the layout without deleting widgets
        for i in reversed(range(self.beat_frame.layout.count())):
            self.beat_frame.layout.itemAt(i).widget().hide()

        # Place start position at the top of the first column if included
        self.beat_frame.layout.addWidget(self.beat_frame.start_pos_view, 0, 0, 1, 1)
        self.beat_frame.start_pos_view.show()

        # Add necessary beat views to the layout
        index = 0
        for row in range(rows):
            for col in range(
                1, columns
            ):  # Start at 1 to reserve space for the start position
                if index < len(self.beats):
                    beat_view = self.beats[index]
                    self.beat_frame.layout.addWidget(beat_view, row, col)
                    beat_view.show()
                    index += 1

        # Update the layout to reflect the new configuration
        self.beat_frame.adjustSize()

    def get_layouts(self) -> dict[int, tuple[int, int]]:
        return {
            0: (1, 1),
            1: (2, 1),
            2: (3, 1),
            3: (4, 1),
            4: (5, 1),
            5: (4, 2),
            6: (4, 2),
            7: (5, 2),
            8: (5, 2),
            9: (4, 3),
            10: (5, 3),
            11: (5, 3),
            12: (4, 4),
            13: (5, 4),
            14: (5, 4),
            15: (5, 4),
            16: (5, 4),
            17: (5, 5),
            18: (5, 5),
            19: (5, 5),
            20: (5, 5),
            21: (5, 6),
            22: (5, 6),
            23: (5, 6),
            24: (5, 6),
            25: (5, 7),
            26: (5, 7),
            27: (5, 7),
            28: (5, 7),
            29: (5, 8),
            30: (5, 8),
            31: (5, 8),
            32: (5, 8),
            33: (5, 9),
            34: (5, 9),
            35: (5, 9),
            36: (5, 9),
            37: (5, 10),
            38: (5, 10),
            39: (5, 10),
            40: (5, 10),
            41: (5, 11),
            42: (5, 11),
            43: (5, 11),
            44: (5, 11),
            45: (5, 12),
            46: (5, 12),
            47: (5, 12),
            48: (5, 12),
            49: (5, 13),
            50: (5, 13),
            51: (5, 13),
            52: (5, 13),
            53: (5, 14),
            54: (5, 14),
            55: (5, 14),
            56: (5, 14),
            57: (5, 15),
            58: (5, 15),
            59: (5, 15),
            60: (5, 15),
            61: (5, 16),
            62: (5, 16),
            63: (5, 16),
            64: (5, 16),
        }
