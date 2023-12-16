from typing import Callable, Dict, List, TYPE_CHECKING
import json
from PyQt6.QtWidgets import QScrollArea, QWidget, QGridLayout
from PyQt6.QtCore import Qt
from constants.string_constants import *
from data.positions_map import get_specific_start_end_positions
from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from widgets.option_picker.option.option import Option
from widgets.sequence_widget.beat_frame.beat import Beat
import pandas as pd

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
        self.options: List[Option] = []
        self.pictographs = self.load_and_sort_data("LetterDictionary.csv")
        self.pictograph = self.main_widget.graph_editor_widget.graph_editor.pictograph
        self.initialize_ui()
        self.viewport().installEventFilter(self)

        self.show_start_position()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def initialize_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.option_picker_layout = QGridLayout(self.container)
        self.container.setContentsMargins(10, 10, 10, 10)  # Set content margins
        self.setWidget(self.container)

    def load_and_sort_data(self, file_path: str) -> pd.DataFrame:
        df = pd.read_csv(file_path)
        df.set_index(["start_position", "end_position"], inplace=True)
        df.sort_index(inplace=True)
        return df

    def show_start_position(self) -> None:
        self.clear_layout()
        start_positions = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, full_key in enumerate(start_positions):
            start_position, end_position = full_key.split("_")
            if (start_position, end_position) in self.pictographs.index:
                row_data = self.pictographs.loc[(start_position, end_position)]
                if isinstance(row_data, pd.DataFrame):
                    row_data = row_data.iloc[0]
                motion_dict = [
                    self.construct_motion_dict(row_data, "blue"),
                    self.construct_motion_dict(row_data, "red"),
                ]

                self.add_option_to_layout(motion_dict, is_initial=True, row=0, col=i)

    def add_option_to_layout(
        self, motion_dict: list, is_initial: bool, row: int, col: int
    ) -> None:
        option = self.create_option(motion_dict)
        event_handler = (
            self.get_initial_handler(option)
            if is_initial
            else self.get_click_handler(option)
        )
        option.view.mousePressEvent = event_handler
        self.option_picker_layout.addWidget(option.view, row, col)

    def get_initial_handler(self, option: "Option") -> Callable:
        return lambda event: self.on_initial_selection(option)

    def get_click_handler(self, option: "Option") -> Callable:
        return lambda event: self.on_option_clicked(option)

    def clear_layout(self) -> None:
        while self.option_picker_layout.count():
            child = self.option_picker_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_initial_selection(self, selected_option: "Option") -> None:
        specific_positions = get_specific_start_end_positions(
            selected_option.motions[RED], selected_option.motions[BLUE]
        )
        self.populate_options(specific_positions["end_position"])

    def populate_options(self, end_position: str) -> None:
        self.options = []
        self.clear_layout()
        self.option_picker_layout.setSpacing(self.spacing)

        # Use .xs to get a cross-section of the data where the first level of the index (start_position) matches the desired value
        filtered_data = self.pictographs.xs(
            end_position, level="start_position", drop_level=False
        )

        for row, ((start_pos, end_pos), row_data) in enumerate(
            filtered_data.iterrows()
        ):
            attributes_list = [
                self.construct_motion_dict(row_data, "blue"),
                self.construct_motion_dict(row_data, "red"),
            ]
            self.add_option_to_layout(
                attributes_list,
                is_initial=False,
                row=row // self.COLUMN_COUNT,
                col=row % self.COLUMN_COUNT,
            )
        self.resize_option_views()

    def create_option(self, motion_dict_list: list) -> "Option":
        option = Option(self.main_widget, self)
        option.setSceneRect(0, 0, 750, 900)
        for motion_dict in motion_dict_list:
            arrow_dict = {
                COLOR: motion_dict[COLOR],
                MOTION_TYPE: motion_dict[MOTION_TYPE],
                TURNS: motion_dict[TURNS],
            }
            prop_dict = {
                COLOR: motion_dict[COLOR],
                PROP_TYPE: self.pictograph.prop_type,
                LOCATION: motion_dict[END_LOCATION],
                LAYER: 1,
                ORIENTATION: IN,
            }
            arrow = Arrow(option, arrow_dict, option.motions[motion_dict[COLOR]])
            prop = Prop(option, prop_dict, option.motions[motion_dict[COLOR]])
            motion_dict[ARROW], motion_dict[PROP] = arrow, prop

            option.motions[motion_dict[COLOR]].arrow = arrow
            option.motions[motion_dict[COLOR]].prop = prop

            option.addItem(arrow)
            option.addItem(prop)
            option.arrows[arrow.color] = arrow
            option.props[prop.color] = prop
            self.setup_motion_relations(option, arrow, prop)
            motion_dict[GHOST_ARROW] = None
            motion_dict[GHOST_PROP] = None
            for motion in option.motions.values():
                if motion.color == motion_dict[COLOR]:
                    motion.setup_attributes(motion_dict)

        self.update_option(option)
        self.options.append(option)
        return option

    def construct_motion_dict(self, row_data, color: str) -> Dict:
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
    def setup_motion_relations(option: Option, arrow: Arrow, prop: Prop) -> None:
        motion = option.motions[arrow.color]
        arrow.motion, prop.motion = motion, motion
        arrow.ghost = option.ghost_arrows[arrow.color]
        arrow.ghost.motion = motion

    @staticmethod
    def update_option(option: "Option") -> None:
        for arrow in option.arrows.values():
            prop = option.props[arrow.color]
            prop.motion = option.motions[arrow.color]
            prop.motion.update_prop_orientation_and_layer()
            prop.update_rotation()
            prop.update_appearance()
            arrow.motion.arrow_location = arrow.motion.determine_arrow_location(
                arrow.motion.start_location, arrow.motion.end_location
            )
        option.update_pictograph()

    def on_option_clicked(self, option: "Option") -> None:
        new_beat = self.copy_scene(option)
        self.main_widget.sequence_widget.beat_frame.add_scene_to_sequence(new_beat)

    def copy_scene(self, option: "Option") -> Beat:
        new_beat = Beat(self.main_widget, self.main_widget.graph_editor_widget)
        new_beat.setSceneRect(option.sceneRect())
        new_beat.motions = option.motions.copy()
        self.duplicate_items(option, new_beat)
        new_beat.update_pictograph()
        return new_beat

    @staticmethod
    def duplicate_items(source_option: Option, target_beat: Beat) -> None:
        for item in source_option.items():
            if isinstance(item, Arrow):
                new_item = Arrow(
                    target_beat, item.get_attributes(), target_beat.motions[item.color]
                )
            elif isinstance(item, Prop):
                new_item = Prop(
                    target_beat, item.get_attributes(), target_beat.motions[item.color]
                )
            else:
                continue
            new_item.setPos(item.pos())
            new_item.setZValue(item.zValue())
            target_beat.addItem(new_item)
            if isinstance(new_item, Arrow):
                target_beat.arrows[new_item.color] = new_item
                new_item.motion = target_beat.motions[new_item.color]
                new_item.ghost = target_beat.ghost_arrows[new_item.color]
                new_item.ghost.motion = new_item.motion
            elif isinstance(new_item, Prop):
                target_beat.props[new_item.color] = new_item
                new_item.motion = target_beat.motions[new_item.color]
                new_item.ghost = target_beat.ghost_props[new_item.color]
                new_item.ghost.motion = new_item.motion

    def resize_option_views(self):
        for option in self.options:
            option.view.resize_option_view()
