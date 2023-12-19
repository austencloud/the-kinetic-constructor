import os
from typing import TYPE_CHECKING, Dict
import pandas as pd
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QScrollArea,
    QCheckBox,
    QHBoxLayout,
    QGridLayout,
    QLabel,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPainter
from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from widgets.image_generator_tab.ig_pictograph import IG_Pictograph
from widgets.image_generator_tab.ig_scroll_area import IG_Scroll_Area

from widgets.option_picker.option.option import Option
from constants.string_constants import (
    COLOR,
    MOTION_TYPE,
    TURNS,
    END_LOCATION,
    IN,
    PROP_TYPE,
    LOCATION,
    LAYER,
    ORIENTATION,
)

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
from typing import List


class ImageGeneratorTab(QWidget):
    imageGenerated = pyqtSignal(str)  # Signal to indicate when an image is generated

    ### INITIALIZATION ###

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.main_pictograph = (
            self.main_widget.graph_editor_widget.graph_editor.main_pictograph
        )
        self.pictograph_df = self.load_and_sort_data("LetterDictionary.csv")
        self.selected_pictographs = []
        self.setupUI()

    ### DATA LOADING ###

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

    ### UI SETUP ###

    def setupUI(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Grid layout for letter checkboxes
        self.letter_checkboxes: Dict[str, QCheckBox] = {}
        checkbox_layout = QGridLayout()
        checkbox_layout.setSpacing(10)

        layout.addLayout(checkbox_layout)

        # Button to generate images
        self.generate_all_button = QPushButton("Generate All Images")
        self.generate_all_button.clicked.connect(self.generate_images_for_all_letters)
        layout.addWidget(self.generate_all_button)

        # Additional button for generating selected images
        self.generate_selected_button = QPushButton("Generate Selected Images")
        self.generate_selected_button.clicked.connect(self.generate_selected_images)
        layout.addWidget(self.generate_selected_button)

        # Improved layout setup
        self.options_layout = QGridLayout()  # Use a grid layout for pictograph options
        layout.addLayout(self.options_layout)

        # Position the buttons more intuitively
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.generate_all_button)
        buttons_layout.addWidget(self.generate_selected_button)
        layout.addLayout(buttons_layout)

        # Create a scroll area for pictograph views
        self.ig_scroll_area = IG_Scroll_Area(self.main_widget, self)

        layout.addWidget(self.ig_scroll_area)

        letters = self.get_letters()
        for i, letter in enumerate(letters):
            checkbox = QCheckBox(letter)
            checkbox.stateChanged.connect(
                lambda checked, ltr=letter: self.on_letter_checkbox_state_changed(
                    checked, ltr
                )
            )

            # Add checkbox to the grid layout
            row = i // self.ig_scroll_area.COLUMN_COUNT
            col = i % self.ig_scroll_area.COLUMN_COUNT
            checkbox_layout.addWidget(checkbox, row, col)
            self.letter_checkboxes[letter] = checkbox

    ### LETTERS ###

    def get_letters(self) -> List[str]:
        return self.pictograph_df.iloc[:, 0].unique().tolist()

    ### IMAGE GENERATION ###

    def on_letter_checkbox_state_changed(self, state, letter) -> None:
        print(f"Checkbox for letter {letter} state changed: {state}")
        if state == 2 and letter not in self.selected_pictographs:
            self.selected_pictographs.append(letter)
        elif state == 0 and letter in self.selected_pictographs:
            self.selected_pictographs.remove(letter)
        self.ig_scroll_area.update_displayed_pictographs()  # Add this line to update the display

    def generate_selected_images(self) -> None:
        for letter in self.selected_pictographs:
            self.generate_images_for_letter(letter)
        self.ig_scroll_area.update_displayed_pictographs()  # Add this line to update the display

    def generate_images_for_all_letters(self) -> None:
        for letter in self.get_letters():
            self.generate_images_for_letter(letter)
        self.ig_scroll_area.update_displayed_pictographs()  # Add this line to update the display

    def generate_images_for_letter(self, letter) -> None:
        # Filter pictographs by letter
        pictographs_for_letter: pd.DataFrame = self.pictograph_df[
            self.pictograph_df["letter"] == letter
        ]

        # Generate an image for each pictograph
        for index, pictograph in pictographs_for_letter.iterrows():
            # Updated to use actual pictograph data
            checkbox_text = f"{pictograph['letter']}_"
            checkbox = QCheckBox(checkbox_text)
            checkbox.stateChanged.connect(
                lambda state, idx=index: self.toggle_pictograph_selection(state, idx)
            )
            self.layout().addWidget(checkbox)
            self.render_pictograph_to_image(pictograph)

    def toggle_pictograph_selection(self, state, index) -> None:
        if state == Qt.CheckState.Checked:
            self.selected_pictographs.append(index)
        else:
            self.selected_pictographs.remove(index)

    def render_pictograph_to_image(self, pictograph) -> None:
        # Create an Option instance from the pictograph data
        option = self._create_option_from_pictograph_data(pictograph)
        option.view.resize_option_view()
        # Render scene to QImage
        image = QImage(
            int(option.width()), int(option.height()), QImage.Format.Format_ARGB32
        )
        painter = QPainter(image)
        option.render(painter)
        painter.end()

        # Save image to file
        image_path = self.get_image_path(pictograph)
        image.save(image_path)
        self.imageGenerated.emit(image_path)

    ### OPTION CREATION ###

    def _create_option_from_pictograph_data(self, pictograph_data) -> Option:
        option = Option(self.main_widget, self)
        option.setSceneRect(0, 0, 750, 900)

        # Use the existing method to create motion dictionaries
        motion_dicts = [
            self._create_motion_dict(pictograph_data, color)
            for color in ["blue", "red"]
        ]

        # Add motions, arrows, and props to the Option instance
        for motion_dict in motion_dicts:
            self._add_motion_to_option(option, motion_dict)
            self._finalize_option_setup(option, motion_dict)

        option.view.resize_option_view()
        option.update_pictograph()

        return option

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

    @staticmethod
    def _setup_motion_relations(option: Option, arrow: Arrow, prop: Prop) -> None:
        motion = option.motions[arrow.color]
        arrow.motion, prop.motion = motion, motion
        arrow.ghost = option.ghost_arrows[arrow.color]
        arrow.ghost.motion = motion

    def _add_motion_to_option(self, option: "Option", motion_dict: Dict) -> None:
        arrow = self._create_arrow(option, motion_dict)
        prop = self._create_prop(option, motion_dict)
        self._setup_motion_relations(option, arrow, prop)

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

    ### IMAGE PATH ###

    def get_image_path(self, pictograph: pd.Series) -> str:
        # Define the root folder
        image_dir = os.path.join(
            "resources", "images", "pictographs", pictograph["letter"]
        )
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        # Construct the image name based on the pictograph attributes
        image_name = (
            f"{pictograph['letter']}_"
            f"{pictograph.name[0]}_"
            f"{pictograph.name[1]}_"
            f"{pictograph['blue_turns']}_"
            f"{pictograph['blue_start_orientation']}_"
            f"{pictograph['blue_end_orientation']}_"
            f"{pictograph['red_turns']}_"
            f"{pictograph['red_start_orientation']}_"
            f"{pictograph['red_end_orientation']}.png"
        )

        return os.path.join(image_dir, image_name)

    ### OPTIONAL ###

    def clear_images(self) -> None:
        # Optional: Clear images if necessary before generation
        pass
