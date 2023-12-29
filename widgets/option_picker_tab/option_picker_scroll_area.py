from typing import Callable, Dict, List, TYPE_CHECKING, Tuple, Union
from PyQt6.QtWidgets import QScrollArea, QWidget, QGridLayout, QApplication
from PyQt6.QtCore import Qt
import pandas as pd
from Enums import Orientation
from data.rules import get_next_letters
from constants import *
from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import Turns
from widgets.option_picker_tab.option import Option
from PyQt6.QtGui import QPixmap


if TYPE_CHECKING:
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
    from widgets.main_widget import MainWidget


class OptionPickerScrollArea(QScrollArea):
    COLUMN_COUNT = 4

    def __init__(
        self,
        main_widget: "MainWidget",
        option_picker_tab: "OptionPickerTab",
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.option_picker_tab = option_picker_tab

        self.spacing = 10
        self.options: List[Tuple[str, Option]] = []
        self.pictographs = self._load_and_sort_data("PictographDataframe.csv")
        self._initialize_ui()
        self._setup_scroll_bars()
        self._connect_signals()

    ### SETUP ###

    def _initialize_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.option_picker_layout = QGridLayout(self.container)
        self.container.setContentsMargins(10, 10, 10, 10)
        self.setWidget(self.container)

    def _setup_scroll_bars(self) -> None:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def _connect_signals(self) -> None:
        self.main_widget.sequence_widget.beat_frame.picker_updater.connect(
            self.update_options
        )

    ### HELPERS ###

    def _load_and_sort_data(self, file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            # Ensure the DataFrame is indexed by 'start_pos' and 'end_pos'
            df.set_index(["start_pos", "end_pos"], inplace=True)
            df.sort_index(inplace=True)
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()

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
        if (start_pos, end_pos) in self.pictographs.index:
            pd_row_data = self.pictographs.loc[(start_pos, end_pos)]
            pd_row_data = (
                pd_row_data.iloc[0]
                if isinstance(pd_row_data, pd.DataFrame)
                else pd_row_data
            )
            start_option = self._create_option(pd_row_data)
            start_option.view.resize_option_view()
            start_option.current_letter = start_option.pd_row_data[LETTER]
            start_option.start_pos = start_option.pd_row_data.name[0]
            start_option.end_pos = start_option.pd_row_data.name[1]
            self._add_option_to_layout(start_option, True, 0, column)

    def _add_option_to_layout(
        self, option: Option, is_start_pos: bool, row: int, col: int
    ) -> None:
        option.view.mousePressEvent = self._get_click_handler(option, is_start_pos)
        self.option_picker_layout.addWidget(option.view, row, col)

    def load_image_if_visible(self, option: "Option") -> None:
        """Loads the image for an option if it is visible."""
        if not option.image_loaded:
            image_path = self.main_widget.generate_image_path(option)

            # If the image is not in cache, check if it exists on disk.
            if image_path not in self.main_widget.image_cache:
                if not os.path.exists(image_path):
                    # If the image does not exist on disk, render and cache it.
                    option.render_and_cache_image()
                else:
                    # If it exists on disk, load it to the cache.
                    self.main_widget.image_cache[image_path] = QPixmap(image_path)

            # Set the pixmap from the cache to the pixmap item of the option.
            if not option.pixmap:
                option.pixmap = option.addPixmap(
                    self.main_widget.image_cache[image_path]
                )
            else:
                option.pixmap.setPixmap(self.main_widget.image_cache[image_path])

            option.image_loaded = True

    def apply_turn_filters(self, filters: Dict[str, Union[Turns, Orientation]]) -> None:
        # self.clear()
        for idx, (letter, option) in enumerate(self.options):
            if option.meets_turn_criteria(filters):
                self._add_option_to_layout(
                    option,
                    is_start_pos=False,
                    row=idx // self.COLUMN_COUNT,
                    col=idx % self.COLUMN_COUNT,
                )

    ### CREATE ###

    def _create_option(self, pd_row_data: pd.Series):
        option = Option(self.main_widget, self)
        option.current_letter = pd_row_data[LETTER]
        filters = self.option_picker_tab.filter_frame.filters
        option._finalize_motion_setup(pd_row_data, filters)
        option.update_pictograph()
        self.load_image_if_visible(option)
        return option

    ### UPDATE ###

    def update_options(self, clicked_option) -> None:
        """Updates the options based on the clicked option."""
        try:
            self._populate_options(clicked_option)
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
        while self.option_picker_layout.count():
            child = self.option_picker_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _populate_options(self, clicked_option: "Option") -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        current_letter = clicked_option.current_letter
        next_possible_letters = get_next_letters(current_letter)
        specific_end_pos = clicked_option.end_pos

        # Filter the DataFrame correctly
        filtered_data = self.pictographs[
            self.pictographs.index.get_level_values(0) == specific_end_pos
        ]
        filtered_data = filtered_data[filtered_data[LETTER].isin(next_possible_letters)]

        self.options.clear()
        self.clear()
        for idx, pd_row_data in filtered_data.iterrows():
            option = self._create_option(pd_row_data)
            self.options.append((pd_row_data[LETTER], option))
        self._sort_options()
        self._add_sorted_options_to_layout()
        QApplication.restoreOverrideCursor()

    def _sort_options(self):
        custom_sort_order = "ABCDEFGHIJKLMNOPQRSTUVWXYZΣΔθΩΦΨΛαβΓ"
        custom_order_dict = {
            char: index for index, char in enumerate(custom_sort_order)
        }
        self.options.sort(key=lambda x: custom_order_dict.get(x[0], float("inf")))

    def _add_sorted_options_to_layout(self):
        for row, (letter, option) in enumerate(self.options):
            option.view.resize_option_view()

            self._add_option_to_layout(
                option,
                is_start_pos=False,
                row=row // self.COLUMN_COUNT,
                col=row % self.COLUMN_COUNT,
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
        self._populate_options(clicked_option)
        new_beat = clicked_option.create_new_beat()
        self.main_widget.sequence_widget.beat_frame.add_scene_to_sequence(new_beat)

    ### RESIZE ###

    def resize_option_picker_scroll(self) -> None:
        for letter, option in self.options:
            option.view.resize_option_view()
