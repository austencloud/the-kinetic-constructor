from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QWidget, QApplication, QHBoxLayout
from PyQt6.QtCore import Qt
from constants import END_POS, LETTER, START_POS
from utilities.TypeChecking.TypeChecking import Letters
from ..pictograph.pictograph import Pictograph
from data.rules import get_next_letters
from ..scroll_area.components.scroll_area_pictograph_factory import (
    ScrollAreaPictographFactory,
)
from ..scroll_area.components.section_manager.section_manager import (
    ScrollAreaSectionManager,
)
from ..scroll_area.components.sequence_builder_display_manager import (
    SequenceBuilderDisplayManager,
)

if TYPE_CHECKING:
    from ..sequence_builder.sequence_builder import SequenceBuilder


class SequenceBuilderScrollArea(QScrollArea):
    def __init__(self, sequence_builder: "SequenceBuilder") -> None:
        super().__init__(sequence_builder)
        self.main_widget = sequence_builder.main_widget
        self.sequence_builder = sequence_builder
        self.letters = self.main_widget.letters
        self.pictographs: dict[Letters, Pictograph] = {}
        self.stretch_index = -1
        self.start_options: dict[str, Pictograph] = {}

        self._setup_ui()
        self._setup_managers()
        self._show_start_pos()

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

    def _setup_managers(self) -> None:
        self.display_manager = SequenceBuilderDisplayManager(self)
        self.sections_manager = ScrollAreaSectionManager(self)
        self.pictograph_factory = ScrollAreaPictographFactory(self)


    ### HELPERS ###

    def _show_start_pos(self) -> None:
        """Shows options for the starting position."""
        self.clear()
        start_pos = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, position_key in enumerate(start_pos):
            self._add_start_pos_option(position_key, i)

    def _add_start_pos_option(self, position_key: str, column: int) -> None:
        """Adds an option for the specified start position."""
        start_pos, end_pos = position_key.split("_")
        for letter, pictograph_dicts in self.letters.items():
            for pictograph_dict in pictograph_dicts:
                if (
                    pictograph_dict[START_POS] == start_pos
                    and pictograph_dict[END_POS] == end_pos
                ):
                    start_option = self.pictograph_factory.create_pictograph()
                    self.start_options[letter] = start_option
                    start_option.letter = letter
                    start_option.start_pos = start_pos
                    start_option.end_pos = end_pos
                    self._add_option_to_layout(start_option, True)
                    start_option.updater.update_pictograph(pictograph_dict)

    def resize_start_options(self, start_options: list[Pictograph]) -> None:
        for start_option in start_options:
            start_option.view.resize_for_scroll_area()

    def _add_option_to_layout(self, option: Pictograph, is_start_pos: bool) -> None:
        option.view.mousePressEvent = self._get_click_handler(option, is_start_pos)
        self.layout.addWidget(option.view)

    def update_options(self, clicked_option) -> None:
        """Updates the options based on the clicked option."""
        try:
            self._update_pictographs(clicked_option)
        except KeyError as e:
            print(f"Motion key missing: {e}")

    def clear(self) -> None:
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().hide()

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
            option = self.pictograph_factory.create_pictograph()
            self.pictographs[motion_dict[LETTER]] = option
        self._sort_options()
        self._add_sorted_options_to_layout()
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

    def _add_sorted_options_to_layout(self) -> None:
        for _, option in self.pictographs.items():
            option.view.resize_for_scroll_area()

            self._add_option_to_layout(
                option,
                row=len(self.pictographs) // self.display_manager.COLUMN_COUNT,
                col=len(self.pictographs) % self.display_manager.COLUMN_COUNT,
                is_start_pos=False,
            )

    ### GETTERS ###

    def _get_click_handler(self, option: "Pictograph", is_start_pos: bool) -> callable:
        """
        Returns a click event handler for an option. This handler updates
        the picker state based on the selected option's attributes.
        """
        if is_start_pos:
            return lambda event: self._on_start_pos_clicked(
                option, self.sequence_builder.filter_tab_manager.filters
            )
        else:
            return lambda event: self._on_option_clicked(option)

    ### EVENT HANDLERS ###

    def _on_start_pos_clicked(self, start_pos: "Pictograph", attributes) -> None:
        self.main_widget.sequence_widget.beat_frame.start_pos_view.set_start_pos(
            start_pos
        )
        self.main_widget.sequence_widget.beat_frame.picker_updater.emit(
            start_pos, attributes
        )

    def _on_option_clicked(self, clicked_option: "Pictograph") -> None:
        self._update_pictographs(clicked_option)
        new_beat = clicked_option.add_to_sequence_manager.create_new_beat()
        self.main_widget.sequence_widget.beat_frame.add_scene_to_sequence(new_beat)

    def resize_sequence_builder_scroll_area(self) -> None:
        self.resize_start_options(list(self.start_options.values()))
