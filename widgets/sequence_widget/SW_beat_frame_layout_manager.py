from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from widgets.sequence_widget.SW_beat_frame.beat import BeatView

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import SW_BeatFrame


class SW_BeatFrameLayoutManager:
    def __init__(self, beat_frame: "SW_BeatFrame"):
        self.beat_frame = beat_frame
        self.selection_manager = beat_frame.selection_manager

    def calculate_layout(self, beat_count: int) -> tuple[int, int]:
        layout_options = self.get_layouts()
        return layout_options.get(beat_count, (1, beat_count))

    def configure_beat_frame(self, num_beats):
        # Assuming a method that calculates the layout based on num_beats
        columns, rows = self.calculate_layout(num_beats)  # +1 for the start position
        self.rearrange_beats(num_beats, columns, rows)
        # update the selection overlay
        selected_beat = self.selection_manager.selected_beat
        if selected_beat:
            self.selection_manager.deselect_beat()
            self.selection_manager.select_beat(selected_beat)
            self.selection_manager.update_overlay_position()
        # turn on the scroll bars if necessary
        self.beat_frame.sequence_widget.scroll_area.verticalScrollBarPolicy = (
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
            if rows > 4
            else Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

    def rearrange_beats(self, num_beats, columns, rows):
        while self.beat_frame.layout.count():
            self.beat_frame.layout.takeAt(0).widget().hide()

        self.beat_frame.layout.addWidget(self.beat_frame.start_pos_view, 0, 0, 1, 1)
        self.beat_frame.start_pos_view.show()

        index = 0
        beats = self.beat_frame.beats
        for row in range(rows):
            for col in range(1, columns + 1):
                if index < num_beats:
                    beat_view = beats[index]
                    self.beat_frame.layout.addWidget(beat_view, row, col)
                    beat_view.show()
                    index += 1
                else:
                    if index < len(beats):
                        beats[index].hide()
                        index += 1

        # if there's a selected beat, update its overlay to its new position
        if self.selection_manager.selected_beat:
            self.selection_manager.update_overlay_position()
            

        # Update the layout to reflect the new configuration
        self.beat_frame.adjustSize()

    def get_layouts(self) -> dict[int, tuple[int, int]]:
        return {
            0: (0, 1),
            1: (1, 1),
            2: (2, 1),
            3: (3, 1),
            4: (4, 1),
            5: (3, 2),
            6: (3, 2),
            7: (4, 2),
            8: (4, 2),
            9: (3, 3),
            10: (5, 2),
            11: (3, 4),
            12: (3, 4),
            13: (4, 4),
            14: (4, 4),
            15: (4, 4),
            16: (4, 4),
            17: (4, 5),
            18: (4, 5),
            19: (4, 5),
            20: (5, 4),
            21: (4, 6),
            22: (4, 6),
            23: (4, 6),
            24: (4, 6),
            25: (4, 7),
            26: (4, 7),
            27: (4, 7),
            28: (4, 7),
            29: (4, 8),
            30: (4, 8),
            31: (4, 8),
            32: (4, 8),
            33: (4, 9),
            34: (4, 9),
            35: (4, 9),
            36: (4, 9),
            37: (4, 10),
            38: (4, 10),
            39: (4, 10),
            40: (4, 10),
            41: (4, 11),
            42: (4, 11),
            43: (4, 11),
            44: (4, 11),
            45: (4, 12),
            46: (4, 12),
            47: (4, 12),
            48: (4, 12),
            49: (4, 13),
            50: (4, 13),
            51: (4, 13),
            52: (4, 13),
            53: (4, 14),
            54: (4, 14),
            55: (4, 14),
            56: (4, 14),
            57: (4, 15),
            58: (4, 15),
            59: (4, 15),
            60: (4, 15),
            61: (4, 16),
            62: (4, 16),
            63: (4, 16),
            64: (4, 16),
        }
