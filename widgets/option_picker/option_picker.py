from typing import Callable, Dict, List, TYPE_CHECKING
import json
from PyQt6.QtWidgets import QScrollArea, QWidget, QGridLayout
from PyQt6.QtCore import QSize, Qt, QEvent
from constants.string_constants import *
from data.positions_map import get_specific_start_end_positions
from objects.arrow import Arrow
from objects.prop import Prop
from widgets.graph_editor.pictograph.pictograph_view import PictographView
from widgets.option_picker.option.option import Option
from widgets.sequence_widget.beat_frame.beat import Beat

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
        self.initialize_ui()
        self.viewport().installEventFilter(self)

        self.pictographs = self.load_json_file("preprocessed.json")
        self.show_initial_selection()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def initialize_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.option_picker_layout = QGridLayout(self.container)
        self.container.setContentsMargins(10, 10, 10, 10)  # Set content margins
        self.setWidget(self.container)

    @staticmethod
    def load_json_file(file_path: str) -> Dict:
        with open(file_path, "r") as file:
            return json.load(file)

    def show_initial_selection(self) -> None:
        self.clear_layout()
        starting_positions = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, position_key in enumerate(starting_positions):
            self.add_option_to_layout(position_key, is_initial=True, row=0, col=i)

    def add_option_to_layout(
        self, position_key: str, is_initial: bool, row: int, col: int
    ) -> None:
        option = self.create_option(self.pictographs[position_key][0][1][:2])
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

    def set_option_view_size(self, view: PictographView) -> None:
        view_width = self.calculate_view_width(self.COLUMN_COUNT)
        view_height = int(view_width * 90 / 75)
        view.setFixedSize(QSize(view_width, view_height))

    def calculate_view_width(self, items_per_row: int) -> int:
        container_width = (
            self.option_picker_widget.width()
            - self.option_picker_widget.button_frame.width()
            - self.option_picker_layout.horizontalSpacing() * (items_per_row - 1)
            - (
                self.container.contentsMargins().left()
                + self.container.contentsMargins().right()
            )
        )
        return int(container_width / items_per_row)

    def clear_layout(self) -> None:
        while self.option_picker_layout.count():
            child = self.option_picker_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_initial_selection(self, selected_option: "Option") -> None:
        specific_positions = get_specific_start_end_positions(
            selected_option.get_motion_by_color(RED),
            selected_option.get_motion_by_color(BLUE),
        )
        self.populate_options(specific_positions["end_position"])

    def populate_options(self, end_position: str) -> None:
        self.options = []
        self.clear_layout()
        self.option_picker_layout.setSpacing(self.spacing)
        for row, (key, _) in enumerate(
            filter(
                lambda item: item[0].startswith(end_position), self.pictographs.items()
            )
        ):
            self.add_option_to_layout(
                key,
                is_initial=False,
                row=row // self.COLUMN_COUNT,
                col=row % self.COLUMN_COUNT,
            )

    def create_option(self, attributes_list: list) -> "Option":
        option = Option(self.main_widget, self)
        option.setSceneRect(0, 0, 750, 900)
        for attribute in attributes_list:
            arrow = Arrow(option, attribute)
            prop = Prop(option, self.get_prop_attributes(attribute[COLOR]))
            option.add_motion(arrow, prop, attribute[MOTION_TYPE], IN, 1)
            option.addItem(arrow)
            option.addItem(prop)
            option.arrows.append(arrow)
            option.props.append(prop)
            self.setup_motion_relations(option, arrow, prop)
        self.update_option(option)
        self.options.append(option)
        return option

    @staticmethod
    def get_prop_attributes(color: str) -> Dict:
        return {
            COLOR: color,
            PROP_TYPE: STAFF,
            PROP_LOCATION: None,
            LAYER: 1,
            ORIENTATION: IN,
        }

    @staticmethod
    def setup_motion_relations(option: Option, arrow: Arrow, prop: Prop) -> None:
        motion = option.get_motion_by_color(arrow.color)
        arrow.motion, prop.motion = motion, motion
        arrow.ghost_arrow, prop.ghost_prop = (
            option.ghost_arrows[arrow.color],
            option.ghost_props[prop.color],
        )
        arrow.ghost_arrow.motion, prop.ghost_prop.motion = motion, motion

    @staticmethod
    def update_option(option: "Option") -> None:
        for arrow in option.arrows:
            prop = option.get_prop_by_color(arrow.color)
            prop.motion = option.get_motion_by_color(arrow.color)
            arrow.prop, prop.arrow = prop, arrow
            prop.motion.update_prop_orientation_and_layer()
            prop.update_rotation()
            prop.update_appearance()
        option.update_pictograph()

    def on_option_clicked(self, option: "Option") -> None:
        new_beat = self.copy_scene(option)
        self.main_widget.sequence.beat_frame.add_scene_to_sequence(new_beat)

    def copy_scene(self, option: "Option") -> Beat:
        new_beat = Beat(self.main_widget, self.main_widget.graph_editor)
        new_beat.setSceneRect(option.sceneRect())
        new_beat.motions = option.motions.copy()
        self.duplicate_items(option, new_beat)
        new_beat.update_pictograph()
        return new_beat

    @staticmethod
    def duplicate_items(source_option: Option, target_beat: Beat) -> None:
        for item in source_option.items():
            if isinstance(item, Arrow):
                new_item = Arrow(target_beat, item.get_attributes())
            elif isinstance(item, Prop):
                new_item = Prop(target_beat, item.get_attributes())
            else:
                continue
            new_item.setPos(item.pos())
            new_item.setZValue(item.zValue())
            target_beat.addItem(new_item)
            if isinstance(new_item, Arrow):
                target_beat.arrows.append(new_item)
                new_item.motion = target_beat.get_motion_by_color(new_item.color)
                new_item.ghost_arrow = target_beat.ghost_arrows[new_item.color]
                new_item.ghost_arrow.motion = new_item.motion
                new_item.prop = target_beat.get_prop_by_color(new_item.color)
            elif isinstance(new_item, Prop):
                target_beat.props.append(new_item)
                new_item.motion = target_beat.get_motion_by_color(new_item.color)
                new_item.ghost_prop = target_beat.ghost_props[new_item.color]
                new_item.ghost_prop.motion = new_item.motion
                new_item.arrow = target_beat.get_arrow_by_color(new_item.color)

