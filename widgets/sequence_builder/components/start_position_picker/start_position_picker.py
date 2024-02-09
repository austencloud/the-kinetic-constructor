from PyQt6.QtWidgets import QWidget, QSizePolicy, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from constants import END_POS, START_POS
from widgets.scroll_area.components.scroll_area_pictograph_factory import (
    ScrollAreaPictographFactory,
)

from widgets.sequence_builder.components.start_position_picker.start_pos_picker_scroll_area import (
    StartPosPickerScrollArea,
)
from ....pictograph.pictograph import Pictograph
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...sequence_builder import SequenceBuilder


class StartPosPicker(QWidget):

    def __init__(self, sequence_builder: "SequenceBuilder", parent=None):
        super().__init__(parent)
        self.sequence_builder = sequence_builder
        self.main_widget = sequence_builder.main_widget
        self.start_options: dict[str, Pictograph] = {}
        self.scroll_area = StartPosPickerScrollArea(self)
        self.pictograph_factory = ScrollAreaPictographFactory(self.scroll_area)
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setup_start_positions()
        self.setStyleSheet("border: 1px solid black;")

    def setup_start_positions(self) -> None:
        """Shows options for the starting position."""
        start_pos = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, position_key in enumerate(start_pos):
            self._add_start_pos_option(position_key, i)

    def on_start_pos_clicked(self, start_pos: "Pictograph") -> None:
        self.sequence_builder.main_widget.sequence_widget.beat_frame.start_pos_view.set_start_pos(
            start_pos
        )
        self.sequence_builder.current_pictograph = start_pos
        self.sequence_builder.transition_to_sequence_building(start_pos)

    def hide_start_positions(self):
        for start_position_pictograph in self.start_options.values():
            start_position_pictograph.view.hide()

    def _add_start_pos_option(self, position_key: str, column: int) -> None:
        """Adds an option for the specified start position."""
        start_pos, end_pos = position_key.split("_")
        for (
            letter,
            pictograph_dicts,
        ) in self.sequence_builder.main_widget.letters.items():
            for pictograph_dict in pictograph_dicts:
                if (
                    pictograph_dict[START_POS] == start_pos
                    and pictograph_dict[END_POS] == end_pos
                ):
                    start_position_pictograph = (
                        self.pictograph_factory.create_pictograph()
                    )
                    self.start_options[letter] = start_position_pictograph
                    start_position_pictograph.letter = letter
                    start_position_pictograph.start_pos = start_pos
                    start_position_pictograph.end_pos = end_pos
                    self.scroll_area._add_option_to_layout(
                        start_position_pictograph, True
                    )
                    start_position_pictograph.updater.update_pictograph(pictograph_dict)

                    # connect to on_start_pos_clicked
                    start_position_pictograph.view.mousePressEvent = (
                        lambda event: self.on_start_pos_clicked(
                            start_position_pictograph
                        )
                    )

    def resize_start_position_picker(self) -> None:
        self.scroll_area.resize_start_pos_picker_scroll_area()
        self._resize_start_position_pictographs()

    def _resize_start_position_pictographs(self):
        for start_option in self.start_options.values():
            view = start_option.view
            view_width = int(
                (
                    view.pictograph.scroll_area.width()
                    / view.pictograph.scroll_area.COLUMN_COUNT
                )
                - view.pictograph.scroll_area.display_manager.SPACING
            )
            view.setMinimumWidth(view_width)
            view.setMaximumWidth(view_width)
            view.setMinimumHeight(view_width)
            view.setMaximumHeight(view_width)

            view.view_scale = view_width / view.pictograph.width()
            view.resetTransform()
            view.scale(view.view_scale, view.view_scale)
