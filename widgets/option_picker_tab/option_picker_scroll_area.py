from typing import Callable, TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from Enums import Letter
from data.rules import get_next_letters
from constants import *
from widgets.option_picker_tab.option import Option
from PyQt6.QtGui import QPixmap

from widgets.pictograph_scroll_area import PictographScrollArea


if TYPE_CHECKING:
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
    from widgets.main_widget import MainWidget


class OptionPickerScrollArea(PictographScrollArea):
    def __init__(
        self, main_widget: "MainWidget", option_picker_tab: "OptionPickerTab"
    ) -> None:
        super().__init__(main_widget, option_picker_tab)
        self.main_widget = main_widget
        self.option_picker_tab = option_picker_tab

        self._connect_signals()
        self._show_start_pos()

    ### SETUP ###

    def _connect_signals(self) -> None:
        self.main_widget.sequence_widget.beat_frame.picker_updater.connect(
            self.update_options
        )

    ### HELPERS ###

    def _show_start_pos(self) -> None:
        """Shows options for the starting position."""
        self.clear()
        start_poss = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, position_key in enumerate(start_poss):
            self._add_start_pos_option(position_key, i)
        self.option_picker_tab.filter_frame.apply_filters()

    def _add_start_pos_option(self, position_key: str, column: int) -> None:
        """Adds an option for the specified start position."""
        start_pos, end_pos = position_key.split("_")
        for letter, motion_dicts in self.letters.items():
            for motion_dict in motion_dicts:
                if (
                    motion_dict[START_POS] == start_pos
                    and motion_dict[END_POS] == end_pos
                ):
                    start_option = self._create_pictograph(motion_dict, OPTION)
                    start_option.current_letter = letter
                    start_option.start_pos = start_pos
                    start_option.end_pos = end_pos
                    self._add_option_to_layout(start_option, 0, column, True)
                    break

    def _add_option_to_layout(
        self, option: Option, row: int, col: int, is_start_pos: bool
    ) -> None:
        option.view.mousePressEvent = self._get_click_handler(option, is_start_pos)
        self.layout.addWidget(option.view, row, col)

    def load_image_if_visible(self, option: "Option") -> None:
        """Loads the image for an option if it is visible."""
        if not option.image_loaded:
            image_path = self.main_widget.generate_image_path(option)

            if image_path not in self.main_widget.image_cache:
                if not os.path.exists(image_path):
                    option.render_and_cache_image()
                else:
                    self.main_widget.image_cache[image_path] = QPixmap(image_path)

            if not option.pixmap:
                option.pixmap = option.addPixmap(
                    self.main_widget.image_cache[image_path]
                )
            else:
                option.pixmap.setPixmap(self.main_widget.image_cache[image_path])

            option.image_loaded = True

    def update_pictographs(self) -> None:
        while self.layout.count():
            widget = self.layout.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()


        # for i, (_, pictograph_data) in enumerate(filtered_pictographs.iterrows()):
        #     option: Option = self._create_pictograph(pictograph_data)
        #     self.load_image_if_visible(option)

        #     row = i // self.COLUMN_COUNT
        #     col = i % self.COLUMN_COUNT
        #     self.layout.addWidget(option.view, row, col)
        #     self.pictographs[option.current_letter] = option
        #     option.update_pictograph()
        #     option.view.resize_option_view()

        self.update_scroll_area_content()

    def update_scroll_area_content(self):
        self.container.adjustSize()
        self.layout.update()
        self.updateGeometry()

    ### UPDATE ###

    def update_options(self, clicked_option) -> None:
        """Updates the options based on the clicked option."""
        try:
            self._update_pictographs(clicked_option)
        except KeyError as e:
            print(f"Motion key missing: {e}")

    @staticmethod
    def _update_option(option: "Option") -> None:
        for arrow in option.arrows.values():
            prop = option.props[arrow.color]
            prop.motion = option.motions[arrow.color]
            prop.motion.update_prop_orientation()
            prop.update_rotation()
            prop.update_appearance()
            arrow.location = arrow.motion.get_arrow_location(
                arrow.motion.start_loc, arrow.motion.end_loc
            )
        option.update_pictograph()

    def clear(self) -> None:
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _update_pictographs(self, clicked_option: "Option") -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        current_letter = clicked_option.current_letter
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
            option = self._create_pictograph(motion_dict, OPTION)
            self.pictographs[motion_dict[LETTER]] = option
        self._sort_options()
        self._add_sorted_options_to_layout()
        QApplication.restoreOverrideCursor()

    def _sort_options(self):
        custom_sort_order = [letter.value for letter in Letter]
        custom_order_dict = {
            char: index for index, char in enumerate(custom_sort_order)
        }
        self.pictographs = dict(
            sorted(
                self.pictographs.items(),
                key=lambda x: custom_order_dict.get(x[1].current_letter, float("inf")),
            )
        )

    def _add_sorted_options_to_layout(self):
        for _, option in self.pictographs.items():
            option.view.resize_option_view()

            self._add_option_to_layout(
                option,
                row=len(self.pictographs) // self.COLUMN_COUNT,
                col=len(self.pictographs) % self.COLUMN_COUNT,
                is_start_pos=False,
            )

    ### GETTERS ###

    def _get_click_handler(self, option: "Option", is_start_pos: bool) -> Callable:
        """
        Returns a click event handler for an option. This handler updates
        the picker state based on the selected option's attributes.
        """
        if is_start_pos:
            return lambda event: self._on_start_pos_clicked(
                option, self.option_picker_tab.filter_frame.filters
            )
        else:
            return lambda event: self._on_option_clicked(option)

    ### EVENT HANDLERS ###

    def _on_start_pos_clicked(self, start_pos: "Option", attributes) -> None:
        self.main_widget.sequence_widget.beat_frame.start_pos_view.set_start_pos(
            start_pos
        )
        self.main_widget.sequence_widget.beat_frame.picker_updater.emit(
            start_pos, attributes
        )

    def _on_option_clicked(self, clicked_option: "Option") -> None:
        self._update_pictographs(clicked_option)
        new_beat = clicked_option.create_new_beat()
        self.main_widget.sequence_widget.beat_frame.add_scene_to_sequence(new_beat)

    ### RESIZE ###

    def resize_option_picker_scroll(self) -> None:
        for letter, option in self.pictographs:
            option.view.resize_option_view()
