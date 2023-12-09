from typing import Callable, Dict, List, TYPE_CHECKING
import json
from PyQt6.QtWidgets import QScrollArea, QWidget, QGridLayout
from PyQt6.QtCore import Qt, QSize
from settings.string_constants import (
    RED,
    BLUE,
    IN,
    OUT,
    COLOR,
    MOTION_TYPE,
    STAFF,
    PROP_TYPE,
    PROP_LOCATION,
    LAYER,
    ORIENTATION,
)
from data.positions_map import get_specific_start_end_positions
from objects.arrow import Arrow
from objects.prop import Prop
from utilities.TypeChecking.TypeChecking import (
    ArrowAttributesDicts,
    DictVariants,
    PropAttributesDicts,
)
from widgets.graph_editor.pictograph.pictograph_view import PictographView

from widgets.option_picker.option.option import Option
from widgets.sequence.beat import Beat

if TYPE_CHECKING:
    from widgets.option_picker.option_picker_widget import OptionPickerWidget
    from widgets.main_widget import MainWidget
from typing import Dict, Any, TextIO


class OptionPicker(QScrollArea):
    COLUMN_COUNT_INITIAL = 3
    COLUMN_COUNT = 4
    MAX_PICTOGRAPHS = 4

    def __init__(
        self, main_widget: "MainWidget", option_picker_widget: "OptionPickerWidget"
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.option_picker_widget = option_picker_widget
        self.spacing = 5
        self.options: List[Option] = []
        self.initialize_ui()
        self.pictographs = self.load_preprocessed_pictographs()
        self.show_initial_selection()

    def initialize_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.option_picker_layout = QGridLayout(self.container)
        self.setWidget(self.container)

    def load_preprocessed_pictographs(self) -> Dict[str, List[List[DictVariants]]]:
        with open("preprocessed.json", "r") as file:
            return json.load(file)

    def show_initial_selection(self) -> None:
        self.clear_layout()
        starting_positions = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, position_key in enumerate(starting_positions):
            self.add_option_to_layout(
                position_key, is_initial=True, row=0, col=i % self.COLUMN_COUNT_INITIAL
            )

    def add_option_to_layout(
        self, position_key: str, is_initial: bool, row: int, col: int
    ) -> None:
        option = self.create_option_from_attributes(
            self.pictographs[position_key][0][1][:2]
        )
        option.view.mousePressEvent = self.get_option_event_handler(option, is_initial)
        self.set_option_view_size(option.view)
        self.option_picker_layout.addWidget(option.view, row, col)

    def get_option_event_handler(self, option, is_initial) -> Callable[..., None]:
        if is_initial:
            return lambda event: self.on_initial_selection(option)
        else:
            return lambda event: self.on_option_clicked(option)

    def set_option_view_size(self, view: PictographView) -> None:
        view_width = self.calculate_view_width(self.COLUMN_COUNT)
        view.setFixedSize(QSize(view_width, int(view_width * 90 / 75)))

    def calculate_view_width(self, items_per_row: int) -> int:
        container_width = (
            self.container.width()
            - self.option_picker_layout.horizontalSpacing() * (items_per_row - 1)
        )
        return int(container_width / items_per_row)

    def clear_layout(self) -> None:
        while self.option_picker_layout.count():
            child = self.option_picker_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_initial_selection(self, selected_option: "Option") -> None:
        # Make sure to handle the event properly
        if selected_option:
            specific_positions = get_specific_start_end_positions(
                selected_option.get_motion_by_color(RED),
                selected_option.get_motion_by_color(BLUE),
            )
            self.populate_options_based_on_selection(specific_positions["end_position"])

    def populate_options_based_on_selection(self, end_position) -> None:
        self.clear_layout()
        self.option_picker_layout.setSpacing(self.spacing)
        row, col = 0, 0

        for key in self.pictographs.keys():
            if key.startswith(end_position):
                self.add_option_to_layout(
                    key, is_initial=False, row=row, col=col % self.COLUMN_COUNT
                )
                col += 1
                if col == self.COLUMN_COUNT:
                    row += 1
                    col = 0

    def create_option_from_attributes(
        self, attributes_list: list[ArrowAttributesDicts]
    ) -> "Option":
        option = Option(self.main_widget, self)
        option.setSceneRect(0, 0, 750, 900)

        for attribute in attributes_list:
            self.create_and_add_motion_to_option(option, attribute)

        self.update_option(option)
        self.options.append(option)
        return option

    def create_and_add_motion_to_option(
        self, option: Option, attribute: ArrowAttributesDicts
    ) -> None:
        arrow = Arrow(option, attribute)
        prop = Prop(option, self.get_prop_attributes(attribute[COLOR]))
        option.add_motion(arrow, prop, attribute[MOTION_TYPE], IN, 1)
        option.addItem(arrow)
        option.addItem(prop)
        self.setup_motion_relations(option, arrow, prop)

    def get_prop_attributes(self, color) -> PropAttributesDicts:
        return {
            COLOR: color,
            PROP_TYPE: STAFF,
            PROP_LOCATION: None,
            LAYER: 1,
            ORIENTATION: IN,
        }

    def setup_motion_relations(self, option: Option, arrow: Arrow, prop: Prop) -> None:
        motion = option.get_motion_by_color(arrow.color)
        arrow.motion, prop.motion = motion, motion
        arrow.ghost_arrow, prop.ghost_prop = (
            option.ghost_arrows[arrow.color],
            option.ghost_props[prop.color],
        )
        arrow.ghost_arrow.motion, prop.ghost_prop.motion = motion, motion
        option.arrows.append(arrow)
        option.props.append(prop)

    def update_option(self, option: "Option") -> None:
        for arrow in option.arrows:
            for prop in option.props:
                if arrow.color == prop.color:
                    arrow.prop, prop.arrow = prop, arrow

        for prop in option.props:
            prop.motion.update_prop_orientation_and_layer()
            prop.update_rotation()
            prop.update_appearance()

        option.update_pictograph()

    def on_option_clicked(self, option: "Option") -> None:
        # Make sure to handle the event properly
        if option:
            self.main_widget.sequence.frame.add_scene_to_sequence(
                self.copy_scene(option)
            )

    def copy_scene(self, option: "Option") -> Beat:
        new_beat = Beat(self.main_widget, self.main_widget.graph_editor)
        new_beat.setSceneRect(option.sceneRect())
        new_beat.motions = option.motions
        self.duplicate_items(option, new_beat)
        new_beat.update_pictograph()
        
        return new_beat

    def duplicate_items(self, source_option: Option, target_beat: Beat) -> None:
        for item in source_option.items():
            if isinstance(item, Arrow):
                self.duplicate_arrow(item, target_beat)
            elif isinstance(item, Prop):
                self.duplicate_prop(item, target_beat)
        for arrow in target_beat.arrows:
            arrow.prop = target_beat.get_prop_by_color(arrow.color)
        for prop in target_beat.props:
            prop.arrow = target_beat.get_arrow_by_color(prop.color)
            


    def duplicate_arrow(self, arrow: Arrow, target_beat: Beat) -> None:
        new_arrow = Arrow(target_beat, arrow.get_attributes())
        self.setup_new_arrow(new_arrow, arrow, target_beat)

    def setup_new_arrow(
        self, new_arrow: Arrow, arrow: Arrow, target_beat: Beat
    ) -> None:
        new_arrow.setPos(arrow.pos())
        new_arrow.setZValue(arrow.zValue())
        target_beat.addItem(new_arrow)
        target_beat.arrows.append(new_arrow)
        ghost_arrow = target_beat.ghost_arrows[new_arrow.color]
        new_arrow.motion = target_beat.get_motion_by_color(new_arrow.color)
        new_arrow.ghost_arrow, ghost_arrow.motion = ghost_arrow, new_arrow.motion

    def duplicate_prop(self, prop: Prop, target_beat: Beat) -> None:
        new_prop = Prop(target_beat, prop.get_attributes())
        self.setup_new_prop(new_prop, prop, target_beat)

    def setup_new_prop(self, new_prop: Prop, prop: Prop, target_beat: Beat) -> None:
        new_prop.setPos(prop.pos())
        new_prop.setZValue(prop.zValue())
        target_beat.addItem(new_prop)
        target_beat.props.append(new_prop)
        ghost_prop = target_beat.ghost_props[new_prop.color]
        new_prop.motion = target_beat.get_motion_by_color(new_prop.color)
        new_prop.ghost_prop, ghost_prop.motion = ghost_prop, new_prop.motion

    def update_option_picker_size(self) -> None:
        self.setFixedWidth(int(self.option_picker_widget.width() * 4 / 5))
        self.setFixedHeight(int(self.option_picker_widget.height()))
        for option in self.options:
            option.view.update_OptionView_size()
