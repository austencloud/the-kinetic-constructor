from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QApplication, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from utilities.TypeChecking.TypeChecking import Letters
from widgets.pictograph.pictograph import Pictograph
from widgets.scroll_area.components.scroll_area_display_manager import (
    ScrollAreaDisplayManager,
)
from data.rules import get_next_letters
from widgets.scroll_area.components.scroll_area_pictograph_factory import (
    ScrollAreaPictographFactory,
)
from widgets.scroll_area.components.section_manager.section_manager import (
    ScrollAreaSectionManager,
)
from constants import *

if TYPE_CHECKING:
    from widgets.sequence_builder.sequence_builder import SequenceBuilder
    from widgets.main_widget.main_widget import MainWidget


class SequenceBuilderScrollArea(QScrollArea):
    def __init__(self, sequence_builder: "SequenceBuilder") -> None:
        super().__init__(sequence_builder)
        self.main_widget = sequence_builder.main_widget
        self.sequence_builder = sequence_builder
        self.letters = self.main_widget.letters
        self.pictographs: dict[Letters, Pictograph] = {}
        self.stretch_index = -1
        self._setup_ui()
        self._setup_managers()
        self._show_start_pos()

    def _setup_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.layout: QHBoxLayout = QHBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.container.setStyleSheet("background-color: #f2f2f2;")
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def _setup_managers(self) -> None:
        self.display_manager = ScrollAreaDisplayManager(self)
        self.sections_manager = ScrollAreaSectionManager(self)
        self.pictograph_factory = ScrollAreaPictographFactory(self)

    def fix_stretch(self):
        if self.stretch_index >= 0:
            item = self.layout.takeAt(self.stretch_index)
            del item
        self.layout.addStretch(1)
        self.stretch_index = self.layout.count()

    def insert_widget_at_index(self, widget: QWidget, index: int) -> None:
        self.layout.insertWidget(index, widget)

    def update_pictographs(self) -> None:
        deselected_letters = self.pictograph_factory.get_deselected_letters()
        selected_letters = set(self.sequence_builder.selected_letters)

        if self._only_deselection_occurred(deselected_letters, selected_letters):
            for letter in deselected_letters:
                self.pictograph_factory.remove_deselected_letter_pictographs(letter)
        else:
            for letter in deselected_letters:
                self.pictograph_factory.remove_deselected_letter_pictographs(letter)
            self.pictograph_factory.process_selected_letters()
        self.display_manager.order_and_display_pictographs()

    def _only_deselection_occurred(self, deselected_letters, selected_letters) -> bool:
        if not deselected_letters:
            return False
        if not selected_letters:
            return True

        current_pictograph_letters = {key.split("_")[0] for key in self.pictographs}

        return (
            len(deselected_letters) > 0
            and len(selected_letters) == len(current_pictograph_letters) - 1
        )

    def update_arrow_placements(self) -> None:
        for pictograph in self.pictographs.values():
            pictograph.arrow_placement_manager.update_arrow_placements()

    ### SETUP ###

    def _connect_signals(self) -> None:
        self.main_widget.main_sequence_widget.beat_frame.picker_updater.connect(
            self.update_options
        )

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
                    start_option = self.pictograph_factory.create_pictograph(OPTION)
                    start_option.letter = letter
                    start_option.start_pos = start_pos
                    start_option.end_pos = end_pos
                    self._add_option_to_layout(start_option, 0, column, True)
                    break

    def _add_option_to_layout(
        self, option: Pictograph, row: int, col: int, is_start_pos: bool
    ) -> None:
        option.view.mousePressEvent = self._get_click_handler(option, is_start_pos)
        self.layout.addWidget(option.view)

    def load_image_if_visible(self, option: "Pictograph") -> None:
        """Loads the image for an option if it is visible."""
        if not option.image_loaded:
            image_path = self.main_widget.image_cache_manager.generate_image_path(
                option
            )

            if image_path not in self.main_widget.image_cache_manager.image_cache:
                if not os.path.exists(image_path):
                    option.image_renderer.render_and_cache_image()
                else:
                    self.main_widget.image_cache_manager.image_cache[image_path] = (
                        QPixmap(image_path)
                    )

            if not option.pixmap:
                option.pixmap = option.addPixmap(
                    self.main_widget.image_cache_manager.image_cache[image_path]
                )
            else:
                option.pixmap.setPixmap(
                    self.main_widget.image_cache_manager.image_cache[image_path]
                )

            option.image_loaded = True

    def update_options(self, clicked_option) -> None:
        """Updates the options based on the clicked option."""
        try:
            self._update_pictographs(clicked_option)
        except KeyError as e:
            print(f"Motion key missing: {e}")

    @staticmethod
    def _update_option(option: "Pictograph") -> None:
        for arrow in option.arrows.values():
            prop = option.props[arrow.color]
            prop.motion = option.motions[arrow.color]
            prop.motion.attr_manager.update_prop_ori()
            prop.updater.update_prop()
            arrow.loc = arrow.location_calculator.get_arrow_location(
                arrow.motion.start_loc, arrow.motion.end_loc, arrow.motion.motion_type
            )
        option.updater.update_pictograph()

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

        # Filter the DataFrame correctly
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
            option = self.pictograph_factory.create_pictograph(OPTION)
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
                option, self.filter_tab_manager.filters
            )
        else:
            return lambda event: self._on_option_clicked(option)

    ### EVENT HANDLERS ###

    def _on_start_pos_clicked(self, start_pos: "Pictograph", attributes) -> None:
        self.main_widget.main_sequence_widget.beat_frame.start_pos_view.set_start_pos(
            start_pos
        )
        self.main_widget.main_sequence_widget.beat_frame.picker_updater.emit(
            start_pos, attributes
        )

    def _on_option_clicked(self, clicked_option: "Pictograph") -> None:
        self._update_pictographs(clicked_option)
        new_beat = clicked_option.add_to_sequence_manager.create_new_beat()
        self.main_widget.main_sequence_widget.beat_frame.add_scene_to_sequence(new_beat)
