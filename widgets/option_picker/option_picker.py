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
from utilities.TypeChecking.TypeChecking import MotionAttributesDicts
from widgets.option_picker.option.option import Option

if TYPE_CHECKING:
    from widgets.option_picker.option_picker_widget import OptionPickerWidget
    from widgets.main_widget import MainWidget


class OptionPicker(QScrollArea):
    COLUMN_COUNT = 4

    def __init__(
        self, main_widget: "MainWidget", option_picker_widget: "OptionPickerWidget"
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.option_picker_widget = option_picker_widget
        self.spacing = 10
        self.options: List[Tuple[Letters, Option]] = []
        self.pictographs = self.load_and_sort_data("LetterDictionary.csv")
        self.pictograph = (
            self.main_widget.graph_editor_widget.graph_editor.main_pictograph
        )
        self.last_end_orientation = None

        self._initialize_ui()
        self.viewport().installEventFilter(self)
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
            # Handle specific exceptions as needed
            print(f"Error loading data: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error

    def show_start_position(self) -> None:
        self.clear()
        start_positions = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, full_key in enumerate(start_positions):
            self._process_position(full_key, i)

    def _process_position(self, full_key: str, column: int) -> None:
        start_position, end_position = full_key.split("_")
        if (start_position, end_position) in self.pictographs.index:
            row_data = self.pictographs.loc[(start_position, end_position)]
            row_data = (
                row_data.iloc[0] if isinstance(row_data, pd.DataFrame) else row_data
            )
            motion_dict = [
                self._create_motion_dict(row_data, color) for color in ["blue", "red"]
            ]
            option = self._create_option(motion_dict)
            self._add_option_to_layout(
                option, is_start_position=True, row=0, col=column
            )

    def _create_option(self, motion_dict_list: list) -> "Option":
        option = Option(self.main_widget, self)
        option.setSceneRect(0, 0, 750, 900)

        for motion_dict in motion_dict_list:
            self._add_motion_to_option(option, motion_dict)
            self._finalize_option_setup(option, motion_dict)

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
            PROP_TYPE: self.pictograph.prop_type,
            LOCATION: motion_dict[END_LOCATION],
            LAYER: 1,
            ORIENTATION: IN,
        }
        prop = Prop(option, prop_dict, option.motions[motion_dict[COLOR]])
        option.props[prop.color] = prop
        prop.motion = option.motions[prop.color]
        option.addItem(prop)
        return prop

    def _finalize_option_setup(self, option: "Option", motion_dict) -> None:
        for motion in option.motions.values():
            if motion.color == motion_dict[COLOR]:
                motion.setup_attributes(motion_dict)
                motion.arrow = option.arrows[motion.color]
                motion.prop = option.props[motion.color]
                motion.assign_location_to_arrow()
                motion.update_prop_orientation_and_layer()
                motion.arrow.set_is_svg_mirrored_from_attributes()
                motion.arrow.update_mirror()
                motion.arrow.update_appearance()
                motion.prop.update_appearance()
                motion.arrow.motion = motion
                motion.prop.motion = motion
                motion.arrow.ghost = option.ghost_arrows[motion.color]
                motion.arrow.ghost.motion = motion
                motion.arrow.ghost.set_is_svg_mirrored_from_attributes()
                motion.arrow.ghost.update_appearance()
                motion.arrow.ghost.update_mirror()
        option.update_pictograph()

    def _create_motion_dict(self, row_data, color: str) -> Dict:
        return {
            "color": row_data[f"{color}_color"],
            "motion_type": row_data[f"{color}_motion_type"],
            "rotation_direction": row_data[f"{color}_rotation_direction"],
            "start_location": row_data[f"{color}_start_location"],
            "end_location": row_data[f"{color}_end_location"],
            "turns": row_data[f"{color}_turns"],
            "start_orientation": row_data[f"{color}_start_orientation"],
            "start_layer": row_data[f"{color}_start_layer"],
        }

    ### UPDATE ###

    def update_options(self, clicked_option) -> None:
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
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)  # Show loading cursor

        # Determine the current letter from the clicked option
        current_letter = clicked_option.letter_engine.get_current_letter()
        next_possible_letters = self._get_next_possible_letters(current_letter)

        # Filter based on the next possible letters
        filtered_data = self.pictographs[
            self.pictographs["letter"].isin(next_possible_letters)
        ]

        # Further filter based on the end position of the clicked option
        specific_end_position = get_specific_start_end_positions(
            clicked_option.motions[RED], clicked_option.motions[BLUE]
        )["end_position"]

        filtered_data = filtered_data[
            (
                filtered_data.index.get_level_values("start_position")
                == specific_end_position
            )
        ]

        # Clear existing options and prepare for new ones
        self.options.clear()
        self.clear()
        self.option_picker_layout.setSpacing(self.spacing)

        # Process filtered data and sort options
        self.options = [
            (row["letter"], self._create_option_from_row(row))
            for _, row in filtered_data.iterrows()
        ]
        self._sort_options()

        # Add sorted options to the layout
        self._add_sorted_options_to_layout()

        QApplication.restoreOverrideCursor()  # Restore default cursor

    def _get_next_possible_letters(self, current_letter: Letters) -> List[Letters]:
        return rules.get(current_letter, [])

    def _create_option_from_row(self, row_data: pd.Series) -> "Option":
        """
        Creates an Option object from a row of the DataFrame.

        Args:
            row_data (pd.Series): The row data from the DataFrame.

        Returns:
            Option: The created Option object.
        """
        option = Option(self.main_widget, self)
        option.setSceneRect(0, 0, 750, 900)

        # Extract motion dictionaries for each color and add to the option
        for color in [RED, BLUE]:
            motion_dict = self._create_motion_dict(row_data, color)
            self._add_motion_to_option(option, motion_dict)

            self._finalize_option_setup(option, motion_dict)
        option.view.resize_option_view()
        option.update_pictograph()

        return option

    def _sort_options(self):
        custom_sort_order = "ABCDEFGHIJKLMNOPQRSTUVWXYZΣΔθΩΦΨΛαβΓ"
        custom_order_dict = {
            char: index for index, char in enumerate(custom_sort_order)
        }
        self.options.sort(key=lambda x: custom_order_dict.get(x[0], float("inf")))

    def _add_sorted_options_to_layout(self):
        for row, (letter, option) in enumerate(self.options):
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


        # Signal the sequence widget to update the picker with new options
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
        red_motion_attributes = clicked_option.motions[RED].get_attributes()
        blue_motion_attributes = clicked_option.motions[BLUE].get_attributes()
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

    def resize_option_picker(self) -> None:
        for letter, option in self.options:
            option.view.resize_option_view()
