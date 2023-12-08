from typing import Dict, List
import json
from PyQt6.QtWidgets import (
    QScrollArea,
    QSizePolicy,
    QFrame,
    QWidget,
    QGridLayout,
)
from typing import TYPE_CHECKING
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
)

from widgets.option_picker.option.option import Option
from widgets.option_picker.option.option_view import OptionView
from widgets.sequence.beat import Beat

if TYPE_CHECKING:
    from widgets.option_picker.option_picker_widget import OptionPickerWidget


class OptionPicker(QScrollArea):
    def __init__(self, option_picker_widget: "OptionPickerWidget") -> None:
        """
        Initialize the OptionPickerScrollArea.

        Args:
            option_picker (OptionPicker): The parent OptionPicker widget.
        """
        super().__init__()
        self.main_window = option_picker_widget.main_window
        self.main_widget = option_picker_widget.main_widget
        self.option_picker_widget = option_picker_widget
        self.scrollbar_width = 0  # Class variable to store the width of the scrollbar
        self.spacing = 16  # Class variable to store the spacing between pictographs
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setWidgetResizable(True)
        self.grid_widget = QWidget()
        self.option_picker_grid_layout = QGridLayout(self.grid_widget)
        self.option_picker_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.option_picker_grid_layout.setSpacing(self.spacing)
        self.setWidget(self.grid_widget)
        self.setFixedWidth(int(self.option_picker_widget.width() * 4 / 5))
        self.setFixedHeight(int(self.option_picker_widget.height()))
        self.options: List[Option] = []
        # Load pictographs from JSON
        with open("preprocessed.json", "r") as file:
            data = json.load(file)

        # Categorize pictographs by letter
        self.pictographs_by_letter = {}
        for pictograph in data:
            letter = data["alpha1_alpha2"][0][0]
            if letter not in self.pictographs_by_letter:
                self.pictographs_by_letter[letter] = []
            self.pictographs_by_letter[letter].append(pictograph)

        self.verticalScrollBar().setFixedWidth(int(self.main_window.width() * 0.01))
        self.populate_pictographs()
        self.update_option_picker_size()

    def populate_pictographs(self):
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
                    option = self.create_Option_from_attributes(arrow_attributes[:2])
                    option_view = option.view
                    option_view.mousePressEvent = (
                        lambda event, opt=option: self.on_option_clicked(opt)
                    )
                    self.option_picker_grid_layout.addWidget(option_view, row, col)
                    col += 1
                    if col >= MAX_ITEMS_PER_ROW:
                        col = 0
                        row += 1
                    pictograph_count += 1  # Increment the pictograph counter
                    self.options.append(option)

    def is_ArrowAttributesDicts(self, attributes: DictVariants) -> bool:
        return COLOR in attributes and MOTION_TYPE in attributes

    def create_Option_from_attributes(
        self, attributes_list: list[ArrowAttributesDicts]
    ) -> Option:
        option = Option(self.main_widget, self)
        option.setSceneRect(0, 0, 750, 900)

        for attributes in attributes_list:
            color = attributes[COLOR]
            motion_type = attributes[MOTION_TYPE]
            arrow = Arrow(option, attributes)
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
            prop.ghost_prop = option.ghost_props[color]
            option.arrows.append(arrow)
            option.props.append(prop)

        for arrow in option.arrows:
            for prop in option.props:
                if arrow.color == prop.color:
                    arrow.prop = prop
                    prop.arrow = arrow

        print("Added motion to option")
        print(option.motions)

        option.update_pictograph()
        return option

    def on_option_clicked(self, option: "Option"):
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
