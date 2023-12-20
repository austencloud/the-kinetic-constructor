from typing import Callable, Dict, List, TYPE_CHECKING, Tuple
from PyQt6.QtWidgets import QScrollArea, QWidget, QGridLayout, QApplication
from PyQt6.QtCore import Qt
import pandas as pd
from data.rules import rules
from constants.string_constants import *
from data.positions_map import get_specific_start_end_positions, positions_map
from objects.arrow.arrow import Arrow
from objects.motion import Motion
from objects.prop.prop import Prop
from utilities.TypeChecking.Letters import Letters
from utilities.TypeChecking.SpecificPositions import SpecificPositions
from utilities.TypeChecking.TypeChecking import MotionAttributesDicts
from widgets.option_picker_tab.option import Option

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
        self.options: List[Tuple[str, Option]] = []
        self.pictographs = self.load_and_sort_data("LetterDictionary.csv")
        self._initialize_ui()
        self.show_start_position()
        self._setup_scroll_bars()
        self._connect_signals()

    def _initialize_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.option_picker_layout = QGridLayout(self.container)
        self.container.setContentsMargins(10, 10, 10, 10)
        self.setWidget(self.container)

    def load_and_sort_data(self, file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
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
            pd_data = self.pictographs.loc[(start_position, end_position)]
            pd_data = pd_data.iloc[0] if isinstance(pd_data, pd.DataFrame) else pd_data
            pictograph_dict = self._create_pictograph_dict(pd_data)
            option = self._create_option_from_pd_data(pd_data)
            option.pictograph_dict = pictograph_dict
            option.view.resize_option_view()
            self._add_option_to_layout(option, True, 0, column)

    def _process_position(self, full_key: str, column: int) -> None:
        start_position, end_position = full_key.split("_")
        if (start_position, end_position) in self.pictographs.index:
            pd_data = self.pictographs.loc[(start_position, end_position)]
            pd_data = pd_data.iloc[0] if isinstance(pd_data, pd.DataFrame) else pd_data
            motion_dict_list = [
                self._create_motion_dict(pd_data, color) for color in ["blue", "red"]
            ]
            pictograph_dict = self._create_pictograph_dict(pd_data)
            option = self._create_option_from_motion_dict_list(
                motion_dict_list, pictograph_dict
            )
            option.pictograph_dict = pictograph_dict
            option.motion_dict_list = motion_dict_list
            self._add_option_to_layout(
                option, is_start_position=True, row=0, col=column
            )

    def _create_pictograph_dict(self, pd_data):
        pictograph_dict = {
            "letter": pd_data.letter,
            "start_position": pd_data.name[0],
            "end_position": pd_data.name[1],
        }
        return pictograph_dict

    def _generate_image_path(self, pd_data: pd.Series) -> str:
        """Generates the image path based on the row data."""
        image_dir = os.path.join(
            "resources", "images", "pictographs", pd_data["letter"]
        )
        image_name = (
            f"{pd_data['letter']}_{pd_data.name[0]}_{pd_data.name[1]}_"
            f"{pd_data['blue_turns']}_{pd_data['blue_start_orientation']}_"
            f"{pd_data['blue_end_orientation']}_{pd_data['red_turns']}_"
            f"{pd_data['red_start_orientation']}_{pd_data['red_end_orientation']}.png"
        )
        return os.path.join(image_dir, image_name)

    def _create_option_from_motion_dict_list(
        self, motion_dict_list: List, pictograph_dict: Dict
    ) -> "Option":
        option = Option(self.main_widget, self)
        option.setSceneRect(0, 0, 750, 900)

        if motion_dict_list:
            image_path = self._generate_image_path(motion_dict_list, pictograph_dict)
            option.loadImage(image_path)

        self.options.append((option.current_letter, option))
        return option

    def _add_motion_to_option(self, option: "Option", motion_dict: Dict) -> None:
        arrow = self._create_arrow(option, motion_dict)
        prop = self._create_prop(option, motion_dict)
        self._setup_motion_relations(option, arrow, prop)

    def _add_option_to_layout(
        self,
        option: Option,
        is_start_position: bool,
        row: int,
        col: int,
    ) -> None:
        option.view.mousePressEvent = self._get_click_handler(option, is_start_position)
        self.option_picker_layout.addWidget(option.view, row, col)

    def _create_arrow(self, option: "Option", motion_dict: Dict) -> Arrow:
        arrow_dict = {
            COLOR: motion_dict[COLOR],
            MOTION_TYPE: motion_dict[MOTION_TYPE],
            TURNS: motion_dict[TURNS],
        }
        arrow = Arrow(option, arrow_dict, option.motions[motion_dict[COLOR]])
        option.arrows[arrow.color] = arrow
        arrow.motion = option.motions[arrow.color]
        option.addItem(arrow)
        return arrow

    def _create_prop(self, option: "Option", motion_dict: Dict) -> Prop:
        prop_dict = {
            COLOR: motion_dict[COLOR],
            PROP_TYPE: self.main_pictograph.prop_type,
            LOCATION: motion_dict[END_LOCATION],
            LAYER: 1,
            ORIENTATION: IN,
        }
        prop = Prop(option, prop_dict, option.motions[motion_dict[COLOR]])
        option.props[prop.color] = prop
        prop.motion = option.motions[prop.color]
        option.addItem(prop)
        return prop

    def _create_motion_dict(self, pd_data: pd.Series, color: str) -> Dict:
        motion_dict = {
            "color": pd_data[f"{color}_color"],
            "motion_type": pd_data[f"{color}_motion_type"],
            "rotation_direction": pd_data[f"{color}_rotation_direction"],
            "start_location": pd_data[f"{color}_start_location"],
            "end_location": pd_data[f"{color}_end_location"],
            "turns": pd_data[f"{color}_turns"],
            "start_orientation": pd_data[f"{color}_start_orientation"],
            "end_orientation": pd_data[f"{color}_end_orientation"],
            "start_layer": pd_data[f"{color}_start_layer"],
            "end_layer": pd_data[f"{color}_end_layer"],
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
        """Populates the options based on the clicked option."""
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        current_letter = clicked_option.pictograph_dict["letter"]
        next_possible_letters = self._get_next_possible_letters(current_letter)
        filtered_data: pd.DataFrame = self.pictographs[
            self.pictographs["letter"].isin(next_possible_letters)
        ]
        specific_end_position = clicked_option.pictograph_dict["end_position"]
        filtered_data = filtered_data[
            filtered_data.index.get_level_values("start_position")
            == specific_end_position
        ]

        self.options.clear()
        self.clear()
        self.options = [
            (pd_data["letter"], self._create_option_from_pd_data(pd_data))
            for _, pd_data in filtered_data.iterrows()
        ]
        self._sort_options()
        self._add_sorted_options_to_layout()
        QApplication.restoreOverrideCursor()

    def _get_next_possible_letters(self, current_letter: Letters) -> List[Letters]:
        return rules.get(current_letter, [])

    def _create_option_from_pd_data(self, pd_data: pd.Series) -> "Option":
        """
        Creates an Option object from a row of the DataFrame.

        Args:
            pd_data (pd.Series): The row data from the DataFrame.

        Returns:
            Option: The created Option object.
        """
        option = Option(self.main_widget, self)
        option.setSceneRect(0, 0, 750, 900)
        motion_dict_list = [
            self._create_motion_dict(pd_data, color) for color in ["blue", "red"]
        ]
        pictograph_dict = self._create_pictograph_dict(pd_data)

        image_path = self._generate_image_path(pd_data)
        option.loadImage(image_path)
        option.motion_dict_list = motion_dict_list
        option.pictograph_dict = pictograph_dict

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
            LAYER: 1,
            ORIENTATION: IN,
        }

    @staticmethod
    def _setup_motion_relations(option: Option, arrow: Arrow, prop: Prop) -> None:
        motion = option.motions[arrow.color]
        arrow.motion, prop.motion = motion, motion
        arrow.ghost = option.ghost_arrows[arrow.color]
        arrow.ghost.motion = motion

    @staticmethod
    def _update_option(option: "Option") -> None:
        for arrow in option.arrows.values():
            prop = option.props[arrow.color]
            prop.motion = option.motions[arrow.color]
            prop.motion.update_prop_orientation_and_layer()
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
