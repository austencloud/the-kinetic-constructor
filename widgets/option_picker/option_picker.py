from typing import Dict, List
import json
from PyQt6.QtWidgets import QScrollArea, QWidget, QGridLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from typing import TYPE_CHECKING
from data.positions_map import get_specific_start_end_positions
from objects.arrow import Arrow
from objects.prop import Prop
from settings.string_constants import (
    BLUE,
    COLOR,
    IN,
    LAYER,
    MOTION_TYPE,
    ORIENTATION,
    PROP_LOCATION,
    PROP_TYPE,
    RED,
    STAFF,
)
from utilities.TypeChecking.TypeChecking import (
    ArrowAttributesDicts,
    DictVariants,
    LetterDictionary,
    PropAttributesDicts,
    SpecificStartEndPositionsDicts,
)

from widgets.option_picker.option.option import Option
from widgets.sequence.beat import Beat

if TYPE_CHECKING:
    from widgets.option_picker.option_picker_widget import OptionPickerWidget
    from widgets.main_widget import MainWidget


class OptionPicker(QScrollArea):
    def __init__(
        self, main_widget: "MainWidget", option_picker_widget: "OptionPickerWidget"
    ):
        super().__init__()
        self.main_widget = main_widget
        self.option_picker_widget = option_picker_widget
        self.spacing = 5
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.option_picker_layout = QGridLayout(self.container)
        self.setWidget(self.container)
        self.pictographs = self.load_preprocessed_pictographs()
        self.show_initial_selection()
        self.options: List[Option] = []

    def load_preprocessed_pictographs(self):
        with open("preprocessed.json", "r") as file:
            return json.load(file)

    def show_initial_selection(self) -> None:
        self.clear_layout(self.option_picker_layout)
        # Set the layout to have 3 columns for the initial options
        column_count = 3
        row = 0
        col = 0

        # Define starting positions (assuming they are part of the JSON keys)
        starting_positions = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, position_key in enumerate(starting_positions):
            self.add_option_to_layout(
                position_key, is_initial=True, row=row, col=i % column_count
            )
            # Update the row index after every third item
            if (i + 1) % column_count == 0:
                row += 1

    def on_initial_selection(self, selected_option: Option) -> None:
        # The user has selected an initial position, now populate the picker based on that choice
        red_motion = selected_option.get_motion_by_color(RED)
        blue_motion = selected_option.get_motion_by_color(BLUE)
        specific_positions: SpecificStartEndPositionsDicts = (
            get_specific_start_end_positions(red_motion, blue_motion)
        )
        end_position = specific_positions["end_position"]
        self.populate_options_based_on_selection(end_position)

    def populate_options_based_on_selection(self, end_position) -> None:
        self.clear_layout(self.option_picker_layout)
        self.option_picker_layout.setSpacing(
            self.spacing
        )  # Set the spacing between items

        # Set fixed column count
        column_count = 4
        row = 0
        col = 0

        for key in self.pictographs.keys():
            if key.startswith(end_position):
                option = self.create_Option_from_attributes_pair(
                    self.pictographs[key][0][1][:2]
                )

                self.option_picker_layout.addWidget(option.view, row, col)

                col += 1
                if col == column_count:
                    row += 1
                    col = 0

    def add_option_to_layout(
        self, position_key: str, is_initial: bool = False, row: int = 0, col: int = 0
    ) -> None:
        # Create an Option from the JSON data
        attributes_pair = self.pictographs[position_key][0][1][
            :2
        ]  # Filter out the optimal position values

        option = self.create_Option_from_attributes_pair(attributes_pair)
        print(f"Created option from attributes pair: {position_key}")
        if is_initial:
            option.view.mousePressEvent = (
                lambda event, opt=option: self.on_initial_selection(opt)
            )
        else:
            # Define what happens when the option is clicked after the initial selection
            option.view.mousePressEvent = (
                lambda event, opt=option: self.on_option_clicked(opt)
            )

        # Calculate the size of the view based on the number of items per row
        column_count = 4  # Set the desired column count
        view_width = self.calculate_view_width(column_count)
        option.view.setFixedSize(QSize(view_width, int(view_width * 90 / 75)))

        # Add the option to the layout at the specified row and column
        self.option_picker_layout.addWidget(option.view, row, col)

    def calculate_view_width(self, items_per_row: int) -> int:
        # Calculate view width based on the container's width and desired aspect ratio
        container_width = (
            self.container.width()
            - self.option_picker_layout.horizontalSpacing() * (items_per_row - 1)
        )
        view_width = int(container_width / items_per_row)
        return view_width

    def clear_layout(self, layout: QGridLayout) -> None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def populate_pictographs(self) -> None:
        with open("preprocessed.json", "r") as file:
            data: Dict = json.load(file)

        pictographs_by_letter: LetterDictionary = {}
        for key, value in data.items():
            for pictograph_data in value:
                letter = pictograph_data[0]
                if letter not in pictographs_by_letter:
                    pictographs_by_letter[letter] = []
                pictographs_by_letter[letter].append(pictograph_data[1])

        row, col = 0, 0
        MAX_ITEMS_PER_ROW = 4
        pictograph_count = 0  # Counter for number of pictographs created
        MAX_PICTOGRAPHS = 4  # Limit for the number of pictographs

        for letter, pictographs in pictographs_by_letter.items():
            for attributes_list in pictographs:
                # Filter out dictionaries that are not arrow attributes
                arrow_attributes = [
                    attr
                    for attr in attributes_list
                    if self.is_ArrowAttributesDicts(attr)
                ]

                if pictograph_count >= MAX_PICTOGRAPHS:
                    break  # Stop if maximum number of pictographs is reached

                if len(arrow_attributes) >= 2:
                    # Process the first two arrow attributes as a pair
                    option = self.create_Option_from_attributes_pair(
                        arrow_attributes[:2]
                    )
                    option_view = option.view
                    option_view.mousePressEvent = (
                        lambda event, opt=option: self.on_option_clicked(opt)
                    )
                    self.option_picker_layout.addWidget(option_view, row, col)
                    col += 1
                    if col >= MAX_ITEMS_PER_ROW:
                        col = 0
                        row += 1
                    pictograph_count += 1  # Increment the pictograph counter
                    self.options.append(option)

    def is_ArrowAttributesDicts(self, attributes: DictVariants) -> bool:
        return COLOR in attributes and MOTION_TYPE in attributes

    def create_Option_from_attributes_pair(
        self, attributes_list: list[ArrowAttributesDicts]
    ) -> Option:
        option = Option(self.main_widget, self)
        option.setSceneRect(0, 0, 750, 900)

        for attribute in attributes_list:
            color = attribute[COLOR]
            motion_type = attribute[MOTION_TYPE]
            arrow = Arrow(option, attribute)
            prop_attributes: PropAttributesDicts = {
                COLOR: color,
                PROP_TYPE: STAFF,
                PROP_LOCATION: None,
                LAYER: 1,
                ORIENTATION: IN,
            }
            prop = Prop(option, prop_attributes)
            option.add_motion(
                arrow,
                prop,
                motion_type,
                IN,
                1,
            )
            option.addItem(arrow)
            option.addItem(prop)
            motion = option.get_motion_by_color(color)
            motion.update_prop_orientation_and_layer()
            arrow.ghost_arrow = option.ghost_arrows[color]
            arrow.ghost_arrow.motion = motion
            prop.ghost_prop = option.ghost_props[color]
            prop.ghost_prop.motion = motion
            option.arrows.append(arrow)
            option.props.append(prop)

        for arrow in option.arrows:
            for prop in option.props:
                if arrow.color == prop.color:
                    arrow.prop = prop
                    prop.arrow = arrow

        for prop in option.props:
            prop.motion.update_prop_orientation_and_layer()
            prop.update_rotation()
            prop.update_appearance()

        option.update_pictograph()
        return option

    def on_option_clicked(self, option: "Option") -> None:
        copied_scene = self.copy_scene(option)
        self.main_widget.sequence.frame.add_scene_to_sequence(copied_scene)

    def copy_scene(self, option: "Option") -> Beat:
        new_beat = Beat(self.main_widget, self.main_widget.graph_editor)
        new_beat.setSceneRect(option.sceneRect())
        new_beat.motions = option.motions

        for item in option.items():
            if isinstance(item, Arrow):
                new_arrow = Arrow(new_beat, item.get_attributes())
                new_arrow.setPos(item.pos())
                new_arrow.setZValue(item.zValue())
                new_beat.addItem(new_arrow)
                new_beat.arrows.append(new_arrow)
                ghost_arrow = new_beat.ghost_arrows[new_arrow.color]
                new_arrow.ghost_arrow = ghost_arrow
                motion = new_beat.get_motion_by_color(new_arrow.color)
                new_arrow.motion = motion
                motion.arrow = new_arrow
                new_arrow.ghost_arrow.motion = new_arrow.motion

            elif isinstance(item, Prop):
                new_prop = Prop(new_beat, item.get_attributes())
                new_prop.setPos(item.pos())
                new_prop.setZValue(item.zValue())
                new_beat.addItem(new_prop)
                new_beat.props.append(new_prop)
                motion = new_beat.get_motion_by_color(new_prop.color)
                ghost_prop = new_beat.ghost_props[new_prop.color]
                new_prop.ghost_prop = ghost_prop
                motion = new_beat.get_motion_by_color(new_prop.color)
                motion.prop = new_prop
                new_prop.motion = motion
                new_prop.ghost_prop.motion = motion

        for arrow in new_beat.arrows:
            for prop in new_beat.props:
                if arrow.color == prop.color:
                    arrow.prop = prop
                    prop.arrow = arrow

        new_beat.update_pictograph()
        return new_beat

    def update_option_picker_size(self) -> None:
        self.setFixedWidth(int(self.option_picker_widget.width() * 4 / 5))
        self.setFixedHeight(int(self.option_picker_widget.height()))
        for option in self.options:
            option.view.update_OptionView_size()
