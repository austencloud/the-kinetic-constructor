from typing import Callable, Dict, List, TYPE_CHECKING, Tuple
from PyQt6.QtWidgets import QScrollArea, QWidget, QGridLayout, QApplication
from PyQt6.QtCore import Qt
import pandas as pd
from data.rules import get_next_letters
from constants.string_constants import *
from widgets.option_picker_tab.option import Option
from PyQt6.QtGui import QPixmap

if TYPE_CHECKING:
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
    from widgets.main_widget import MainWidget


class OptionPickerScroll(QScrollArea):
    COLUMN_COUNT = 4


class OptionPickerScroll(QScrollArea):
    COLUMN_COUNT = 4

    def __init__(
        self, main_widget: "MainWidget", option_picker_widget: "OptionPickerTab"
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.option_picker_widget = option_picker_widget
        self.spacing = 10
        self.image_cache = {}  # Add an image cache
        self.options: List[Tuple[str, Option]] = []
        self.pictographs = self.load_and_sort_data("LetterDictionary.csv")
        self._initialize_ui()
        self.show_start_position()
        self._setup_scroll_bars()
        self._connect_signals()
        self.pixmap_cache = {}

    def get_cached_pixmap(self, image_path: str) -> QPixmap | None:
        return self.pixmap_cache.get(image_path)

    def cache_pixmap(self, image_path: str, pixmap: QPixmap) -> None:
        self.pixmap_cache[image_path] = pixmap

    def _initialize_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.option_picker_layout = QGridLayout(self.container)
        self.container.setContentsMargins(10, 10, 10, 10)
        self.setWidget(self.container)

    def load_and_sort_data(self, file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            # Ensure the DataFrame is indexed by 'start_position' and 'end_position'
            df.set_index(["start_position", "end_position"], inplace=True)
            df.sort_index(inplace=True)
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()

    def show_start_position(self) -> None:
        """Shows options for the starting position."""
        self.clear()
        start_positions = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, position_key in enumerate(start_positions):
            self._add_start_position_option(position_key, i)

    def _add_start_position_option(self, position_key: str, column: int) -> None:
        """Adds an option for the specified start position."""
        start_position, end_position = position_key.split("_")
        if (start_position, end_position) in self.pictographs.index:
            pd_row_data = self.pictographs.loc[(start_position, end_position)]
            pd_row_data = (
                pd_row_data.iloc[0]
                if isinstance(pd_row_data, pd.DataFrame)
                else pd_row_data
            )
            start_option = self._create_option(pd_row_data)
            start_option.view.resize_option_view()
            start_option.current_letter = start_option.pd_row_data["letter"]
            start_option.start_position = start_option.pd_row_data.name[0]
            start_option.end_position = start_option.pd_row_data.name[1]
            self._add_option_to_layout(start_option, True, 0, column)

    def _create_pictograph_dict(self, pd_row_data):
        pictograph_dict = {
            "letter": pd_row_data.letter,
            "start_position": pd_row_data.name[0],
            "end_position": pd_row_data.name[1],
        }
        return pictograph_dict

    def _generate_image_path(self, option: Option) -> str:
        """Generates the image path based on the row data."""
        pd_row_data = option.pd_row_data

        image_dir = os.path.join(
            "resources",
            "images",
            "pictographs",
            pd_row_data["letter"],
            option.main_widget.prop_type,
        )

        image_name = (
            f"{pd_row_data['letter']}_{pd_row_data.name[0]}_{pd_row_data.name[1]}_"
            f"{pd_row_data['blue_turns']}_{pd_row_data['blue_start_orientation']}_"
            f"{pd_row_data['blue_end_orientation']}_{pd_row_data['red_turns']}_"
            f"{pd_row_data['red_start_orientation']}_{pd_row_data['red_end_orientation']}_"
            f"{option.main_widget.prop_type}.png"
        )
        return os.path.join(image_dir, image_name)

    def _add_option_to_layout(
        self, option: Option, is_start_position: bool, row: int, col: int
    ) -> None:
        option.view.mousePressEvent = self._get_click_handler(option, is_start_position)
        self.option_picker_layout.addWidget(option.view, row, col)

    def load_image_if_visible(self, option: "Option") -> None:
        """Loads the image for an option if it is visible."""
        if not option.imageLoaded and option.view.isVisible():
            image_path = self._generate_image_path(option)
            if image_path not in self.image_cache:
                self.image_cache[image_path] = QPixmap(image_path)
            option.pixmapItem = option.addPixmap(self.image_cache[image_path])

    def _create_motion_dict(self, pd_row_data: pd.Series, color: str) -> Dict:
        motion_dict = {
            "color": color,
            "motion_type": pd_row_data[f"{color}_motion_type"],
            "rotation_direction": pd_row_data[f"{color}_rotation_direction"],
            "start_location": pd_row_data[f"{color}_start_location"],
            "end_location": pd_row_data[f"{color}_end_location"],
            "turns": pd_row_data[f"{color}_turns"],
            "start_orientation": pd_row_data[f"{color}_start_orientation"],
            "end_orientation": pd_row_data[f"{color}_end_orientation"],
        }
        return motion_dict

    ### UPDATE ###

    def update_options(self, clicked_option) -> None:
        """Updates the options based on the clicked option."""
        try:
            self._populate_options(clicked_option)
        except KeyError as e:
            print(f"Motion key missing: {e}")

    def clear(self) -> None:
        while self.option_picker_layout.count():
            child = self.option_picker_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _populate_options(self, clicked_option: "Option") -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        current_letter = clicked_option.current_letter
        next_possible_letters = get_next_letters(current_letter)
        specific_end_position = clicked_option.end_position

        # Filter the DataFrame correctly
        filtered_data = self.pictographs[
            self.pictographs.index.get_level_values(0) == specific_end_position
        ]
        filtered_data = filtered_data[
            filtered_data["letter"].isin(next_possible_letters)
        ]

        # filter to ensure the options have a start orientation for each motion that matches the end orientations of the reference option's motions
        for color in [BLUE, RED]:
            filtered_data = filtered_data[
                filtered_data[f"{color}_start_orientation"]
                == clicked_option.motions[color].end_orientation
            ]

        self.options.clear()
        self.clear()
        for idx, pd_row_data in filtered_data.iterrows():
            option = self._create_option(pd_row_data)
            self.options.append((pd_row_data["letter"], option))
        self._sort_options()
        self._add_sorted_options_to_layout()
        QApplication.restoreOverrideCursor()

    def _create_option(self, pd_row_data: pd.Series):
        letter = pd_row_data["letter"]
        option = Option(self.main_widget, self)
        option.setSceneRect(0, 0, 950, 950)
        option.pd_row_data = pd_row_data
        image_path = self._generate_image_path(option)
        option.loadImage(image_path)
        self.load_image_if_visible(option)

        # Setup option attributes
        # Instead of a comprehension, explicitly create each motion_dict
        blue_motion_dict = self._create_motion_dict(pd_row_data, "blue")
        red_motion_dict = self._create_motion_dict(pd_row_data, "red")

        option.motions[RED].setup_attributes(red_motion_dict)
        option.motions[BLUE].setup_attributes(blue_motion_dict)

        option.current_letter = letter
        option.start_position = pd_row_data.name[0]
        option.end_position = pd_row_data.name[1]
        option.motions[RED].arrow = option.arrows[RED]
        option.motions[BLUE].arrow = option.arrows[BLUE]
        option.motions[RED].prop = option.props[RED]
        option.motions[BLUE].prop = option.props[BLUE]
        option.motions[RED].arrow.location = option.motions[RED].get_arrow_location(
            option.motions[RED].start_location, option.motions[RED].end_location
        )
        option.motions[BLUE].arrow.location = option.motions[BLUE].get_arrow_location(
            option.motions[BLUE].start_location, option.motions[BLUE].end_location
        )
        option.motions[RED].update_prop_orientation()
        option.motions[BLUE].update_prop_orientation()
        option.current_letter = pd_row_data["letter"]
        option.start_position = pd_row_data.name[0]
        option.end_position = pd_row_data.name[1]

        option.arrows[RED].motion_type = pd_row_data["red_motion_type"]
        option.arrows[BLUE].motion_type = pd_row_data["blue_motion_type"]
        option.motions[RED].motion_type = pd_row_data["red_motion_type"]
        option.motions[BLUE].motion_type = pd_row_data["blue_motion_type"]

        self._setup_motion_relations(option)

        return option

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
                is_start_position=False,
                row=row // self.COLUMN_COUNT,
                col=row % self.COLUMN_COUNT,
            )

    ### GETTERS ###

    def _get_click_handler(self, option: "Option", is_start_position: bool) -> Callable:
        """
        Returns a click event handler for an option. This handler updates
        the picker state based on the selected option's attributes.
        """
        if is_start_position:
            return lambda event: self._on_start_position_clicked(option)
        else:
            return lambda event: self._on_option_clicked(option)

    def _on_start_position_clicked(self, start_position: "Option") -> None:
        self.main_widget.sequence_widget.beat_frame.start_position_view.set_start_position(
            start_position
        )
        self.main_widget.sequence_widget.beat_frame.picker_updater.emit(start_position)

    @staticmethod
    def get_prop_attributes(color: str) -> Dict:
        return {
            COLOR: color,
            PROP_TYPE: STAFF,
            LOCATION: None,
            ORIENTATION: IN,
        }

    @staticmethod
    def _setup_motion_relations(option: "Option") -> None:
        for color in [RED, BLUE]:
            option.motions[color].arrow = option.arrows[color]
            option.motions[color].prop = option.props[color]
            option.motions[color].arrow.location = option.motions[
                color
            ].get_arrow_location(
                option.motions[color].start_location, option.motions[color].end_location
            )
            option.motions[color].update_prop_orientation()

    @staticmethod
    def _update_option(option: "Option") -> None:
        for arrow in option.arrows.values():
            prop = option.props[arrow.color]
            prop.motion = option.motions[arrow.color]
            prop.motion.update_prop_orientation()
            prop.update_rotation()
            prop.update_appearance()
            arrow.location = arrow.motion.get_arrow_location(
                arrow.motion.start_location, arrow.motion.end_location
            )
        option.update_pictograph()

    def _on_option_clicked(self, clicked_option: "Option") -> None:
        self._populate_options(clicked_option)
        new_beat = clicked_option.create_new_beat()
        self.main_widget.sequence_widget.beat_frame.add_scene_to_sequence(new_beat)

    def _setup_scroll_bars(self) -> None:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def _connect_signals(self) -> None:
        self.main_widget.sequence_widget.beat_frame.picker_updater.connect(
            self.update_options
        )

    def resize_option_picker_scroll(self) -> None:
        for letter, option in self.options:
            option.view.resize_option_view()
