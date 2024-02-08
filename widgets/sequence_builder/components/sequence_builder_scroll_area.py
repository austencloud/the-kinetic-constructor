from typing import TYPE_CHECKING
from constants import LETTER
from PyQt6.QtWidgets import QScrollArea, QWidget, QApplication, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from utilities.TypeChecking.TypeChecking import Letters
from ...pictograph.pictograph import Pictograph
from data.rules import get_next_letters

if TYPE_CHECKING:
    from ..sequence_builder import SequenceBuilder


class SequenceBuilderScrollArea(QScrollArea):
    def __init__(self, sequence_builder: "SequenceBuilder") -> None:
        super().__init__(sequence_builder)
        self.main_widget = sequence_builder.main_widget
        self.sequence_builder = sequence_builder
        self.clickable_option_handler = sequence_builder.clickable_option_handler
        self.display_manager = sequence_builder.display_manager
        self.sections_manager = sequence_builder.sections_manager
        self.letters = self.main_widget.letters
        self.pictographs: dict[Letters, Pictograph] = {}
        self.stretch_index = -1
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.layout: QHBoxLayout = QHBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.container.setStyleSheet("background-color: #f2f2f2;")
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def clear(self) -> None:
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().hide()

    def _add_option_to_layout(self, option: Pictograph, is_start_pos: bool) -> None:
        option.view.mousePressEvent = self.clickable_option_handler._get_click_handler(
            option, is_start_pos
        )
        self.layout.addWidget(option.view)

    def resize_sequence_builder_scroll_area(self) -> None:
        self.setMinimumWidth(self.main_widget.main_tab_widget.width())
        self.sequence_builder.start_position_handler.resize_start_options()

    def _update_pictographs(self, clicked_option: "Pictograph") -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        current_letter = clicked_option.letter
        next_possible_letters = get_next_letters(current_letter)
        specific_end_pos = clicked_option.end_pos

        filtered_data = [
            motion_dict
            for motion_dict_collection in self.main_widget.letters.values()
            for motion_dict in motion_dict_collection
            if motion_dict["end_pos"] == specific_end_pos
            and motion_dict[LETTER] in next_possible_letters
        ]

        self.pictographs.clear()
        self.clear()
        for motion_dict in filtered_data:
            option = self.sequence_builder.pictograph_factory.create_pictograph()
            self.pictographs[motion_dict[LETTER]] = option
        self._sort_options()
        self._add_sorted_pictographs_to_scroll_area()
        QApplication.restoreOverrideCursor()

    def _sort_options(self):
        custom_sort_order = [letter for letter in Letters.__members__.values()]
        custom_order_dict = {
            char: index for index, char in enumerate(custom_sort_order)
        }
        self.pictographs = dict(
            sorted(
                self.pictographs.items(),
                key=lambda x: custom_order_dict.get(x[1].letter, float("inf")),
            )
        )

    def _add_sorted_pictographs_to_scroll_area(self) -> None:
        for _, option in self.pictographs.items():
            option.view.resize_for_scroll_area()

            self._add_option_to_layout(
                option,
                row=len(self.pictographs) // self.display_manager.COLUMN_COUNT,
                col=len(self.pictographs) % self.display_manager.COLUMN_COUNT,
                is_start_pos=False,
            )
