import os
from typing import TYPE_CHECKING, Dict, Union
import pandas as pd
from PyQt6.QtWidgets import (
    QWidget,
    QSplitter,
    QVBoxLayout,
    QPushButton,
    QScrollArea,
    QCheckBox,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
    QApplication,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPainter
from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import Orientations, Turns
from widgets.image_generator_tab.ig_filter_frame import IGFilterFrame
from widgets.image_generator_tab.ig_letter_button_frame import IGLetterButtonFrame
from widgets.image_generator_tab.ig_pictograph import IGPictograph
from widgets.image_generator_tab.ig_scroll import IGScroll

from constants.string_constants import (
    BLUE,
    COLOR,
    MOTION_TYPE,
    RED,
    START_ORIENTATION,
    TURNS,
    END_LOCATION,
    IN,
    PROP_TYPE,
    LOCATION,
    ORIENTATION,
)

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
from typing import List


class IGTab(QWidget):
    imageGenerated = pyqtSignal(str)  # Signal to indicate when an image is generated

    ### INITIALIZATION ###

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.main_pictograph = (
            self.main_widget.graph_editor_tab.graph_editor.main_pictograph
        )
        self.pictograph_df = self.load_and_sort_data("PictographDataframe.csv")
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
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setLayout(self.layout)
        button_frame = QFrame()
        button_frame_layout = QVBoxLayout()
        self.letter_button_frame = IGLetterButtonFrame(self.main_widget)
        action_button_frame = QFrame()
        self.ig_scroll_area = IGScroll(self.main_widget, self)
        self.filter_frame = IGFilterFrame(self)
        self.letter_button_frame.setStyleSheet(
            """
            QFrame {
                border: 1px solid black;
            }
            """
        )
        action_button_frame_layout = QVBoxLayout()
        button_frame_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.generate_all_button = QPushButton("Generate All Images 🧨", self)
        self.generate_all_button.setStyleSheet("font-size: 16px;")
        self.generate_selected_button = QPushButton("Generate Selected Images", self)
        self.generate_selected_button.setStyleSheet("font-size: 16px;")
        self.layout.addWidget(self.letter_button_frame)

        self.generate_all_button.clicked.connect(self.generate_images_for_all_letters)
        self.generate_selected_button.clicked.connect(self.generate_selected_images)

        action_button_frame.setLayout(action_button_frame_layout)
        button_frame.setLayout(button_frame_layout)
        button_frame.setStyleSheet(
            """
            QFrame {
                border: 1px solid black;
            }
            """
        )
        button_frame.setContentsMargins(0, 0, 0, 0)
        button_frame_layout.setContentsMargins(0, 0, 0, 0)
        button_frame_layout.setSpacing(0)
        action_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        action_button_frame_layout.setSpacing(0)
        action_button_frame_layout.addWidget(self.generate_all_button)
        action_button_frame_layout.addWidget(self.generate_selected_button)
        button_frame_layout.addWidget(self.letter_button_frame, 8)
        button_frame_layout.addWidget(action_button_frame, 1)
        self.layout.addWidget(self.ig_scroll_area)
        self.layout.addWidget(button_frame)
        letters = self.get_letters()
        letters.sort(
            key=lambda x: x
            if x not in ["Σ", "Δ", "θ", "Ω", "Φ", "Ψ", "Λ", "α", "β", "Γ"]
            else chr(ord(x) + 1000)
        )

        for key, button in self.letter_button_frame.buttons.items():
            button.clicked.connect(
                lambda checked, letter=key: self.on_letter_button_clicked(letter)
            )

    ### LETTERS ###

    def get_button_style(self, pressed: bool) -> str:
        if pressed:
            # Here you can define your custom style for the pressed state
            return """
                QPushButton {
                    background-color: #ccd9ff;
                    border: 2px solid #0000ff;
                    padding: 5px;
                }
            """
        else:
            # Here you define the default style
            return """
                QPushButton {
                    background-color: white;
                    border: 1px solid black;
                    padding: 0px;
                }
                QPushButton:hover {
                    background-color: #e6f0ff;
                }
                QPushButton:pressed {
                    background-color: #cce0ff;
                }
            """

    def get_letters(self) -> List[str]:
        return self.pictograph_df.iloc[:, 0].unique().tolist()

    ### IMAGE GENERATION ###

    def on_letter_button_clicked(self, letter) -> None:
        print(f"Button for letter {letter} clicked")
        button = self.letter_button_frame.buttons[letter]

        if letter in self.selected_pictographs:
            self.selected_pictographs.remove(letter)
            button.setFlat(False)  # This makes the button appear not pressed
            button.setStyleSheet(self.get_button_style(pressed=False))
        else:
            self.selected_pictographs.append(letter)
            button.setFlat(True)  # This makes the button appear pressed
            button.setStyleSheet(self.get_button_style(pressed=True))

        self.ig_scroll_area.update_displayed_pictographs()

    def on_letter_checkbox_state_changed(self, state, letter) -> None:
        print(f"Checkbox for letter {letter} state changed: {state}")
        if state and letter not in self.selected_pictographs:
            self.selected_pictographs.append(letter)
        elif not state and letter in self.selected_pictographs:
            self.selected_pictographs.remove(letter)
        self.ig_scroll_area.update_displayed_pictographs()  # Add this line to update the display

    def generate_selected_images(self) -> None:
        main_widget = self.parentWidget()  # Access the main widget
        main_widget.setEnabled(False)  # Disable the widget
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)  # Show loading cursor
        self.setMouseTracking(False)  # Ignore mouse clicks
        for letter in self.selected_pictographs:
            self.generate_images_for_letter(letter)
        main_widget.setEnabled(True)  # Enable the widget after generation
        QApplication.restoreOverrideCursor()
        self.setMouseTracking(True)  # Enable mouse clicks

    def generate_images_for_all_letters(self) -> None:
        main_widget = self.parentWidget()  # Access the main widget
        main_widget.setEnabled(False)  # Disable the widget
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)  # Show loading cursor
        self.setMouseTracking(False)  # Ignore mouse clicks
        for letter in self.get_letters():
            self.generate_images_for_letter(letter)
        main_widget.setEnabled(True)  # Enable the widget after generation
        QApplication.restoreOverrideCursor()

        self.setMouseTracking(True)  # Enable mouse clicks

    def generate_images_for_letter(self, letter) -> None:
        pictographs_for_letter: pd.DataFrame = self.pictograph_df[
            self.pictograph_df["letter"] == letter
        ]

        for index, pictograph_data in pictographs_for_letter.iterrows():
            self.render_pictograph_to_image(pictograph_data)

    def toggle_pictograph_selection(self, state, index) -> None:
        if state == Qt.CheckState.Checked:
            self.selected_pictographs.append(index)
        else:
            self.selected_pictographs.remove(index)

    def render_pictograph_to_image(self, pd_row_data) -> None:
        ig_pictograph = self._create_ig_pictograph(pd_row_data)
        ig_pictograph.update_pictograph()

        prop_type = self.main_widget.prop_type
        letter = pd_row_data["letter"]

        if pd_row_data["blue_motion_type"] == "pro":
            blue_motion_type_prefix = "p"
        elif pd_row_data["blue_motion_type"] == "anti":
            blue_motion_type_prefix = "a"
        elif pd_row_data["blue_motion_type"] == "static":
            blue_motion_type_prefix = "s"
        elif pd_row_data["blue_motion_type"] == "dash":
            blue_motion_type_prefix = "d"

        if pd_row_data["red_motion_type"] == "pro":
            red_motion_type_prefix = "p"
        elif pd_row_data["red_motion_type"] == "anti":
            red_motion_type_prefix = "a"
        elif pd_row_data["red_motion_type"] == "static":
            red_motion_type_prefix = "s"
        elif pd_row_data["red_motion_type"] == "dash":
            red_motion_type_prefix = "d"

        blue_turns = self.filter_frame.filters["left_turns"]
        red_turns = self.filter_frame.filters["right_turns"]

        # Construct the folder name based on turns and motion types
        turns_folder = f"({blue_motion_type_prefix}{blue_turns},{red_motion_type_prefix}{red_turns})"

        image_dir = os.path.join(
            "resources",
            "images",
            "pictographs",
            letter,
            prop_type,
            turns_folder,
        )
        os.makedirs(image_dir, exist_ok=True)
        blue_end_orientation = ig_pictograph.motions[BLUE].get_end_orientation()
        red_end_orientation = ig_pictograph.motions[RED].get_end_orientation()

        # Modify the filename to include motion types and turns
        image_name = (
            f"{letter}_"
            f"({pd_row_data.name[0]}→{pd_row_data.name[1]})_"
            f"({pd_row_data['blue_start_location']}→{pd_row_data['blue_end_location']}_"
            f"{blue_turns}_"
            f"{pd_row_data['blue_start_orientation']}_{blue_end_orientation})_"
            f"({pd_row_data['red_start_location']}→{pd_row_data['red_end_location']}_"
            f"{red_turns}_"
            f"{pd_row_data['red_start_orientation']}_{red_end_orientation})_"
            f"{prop_type}.png "
        )

        image_path = os.path.join(image_dir, image_name)
        image = QImage(
            int(ig_pictograph.width()),
            int(ig_pictograph.height()),
            QImage.Format.Format_ARGB32,
        )
        painter = QPainter(image)
        ig_pictograph.render(painter)
        painter.end()

        # Save the image
        try:
            image.save(image_path)
            self.imageGenerated.emit(image_path)
        except Exception as e:
            print(f"Failed to save image: {e}")

    ### OPTION CREATION ###

    def _create_ig_pictograph(self, pd_row_data: pd.Series):
        letter = pd_row_data["letter"]
        ig_pictograph = IGPictograph(self.main_widget, self.ig_scroll_area)
        ig_pictograph.setSceneRect(0, 0, 950, 950)

        ig_pictograph._finalize_motion_setup(pd_row_data, self.filter_frame.filters)

        blue_motion_dict = ig_pictograph._create_motion_dict_from_pd_row_data(
            pd_row_data, "blue", self.filter_frame.filters
        )
        red_motion_dict = ig_pictograph._create_motion_dict_from_pd_row_data(
            pd_row_data, "red", self.filter_frame.filters
        )

        ig_pictograph.props[RED].ghost = ig_pictograph.ghost_props[RED]
        ig_pictograph.props[BLUE].ghost = ig_pictograph.ghost_props[BLUE]
        ig_pictograph.motions[RED].prop = ig_pictograph.props[RED]
        ig_pictograph.motions[BLUE].prop = ig_pictograph.props[BLUE]

        ig_pictograph.motions[RED].setup_attributes(red_motion_dict)
        ig_pictograph.motions[BLUE].setup_attributes(blue_motion_dict)

        ig_pictograph.current_letter = letter
        ig_pictograph.start_position = pd_row_data.name[0]
        ig_pictograph.end_position = pd_row_data.name[1]
        
        ig_pictograph.motions[RED].arrow = ig_pictograph.arrows[RED]
        ig_pictograph.motions[BLUE].arrow = ig_pictograph.arrows[BLUE]
        ig_pictograph.motions[RED].prop = ig_pictograph.props[RED]
        ig_pictograph.motions[BLUE].prop = ig_pictograph.props[BLUE]
        ig_pictograph.motions[RED].arrow.location = ig_pictograph.motions[
            RED
        ].get_arrow_location(
            ig_pictograph.motions[RED].start_location,
            ig_pictograph.motions[RED].end_location,
        )
        ig_pictograph.motions[BLUE].arrow.location = ig_pictograph.motions[
            BLUE
        ].get_arrow_location(
            ig_pictograph.motions[BLUE].start_location,
            ig_pictograph.motions[BLUE].end_location,
        )

        ig_pictograph.arrows[RED].motion_type = pd_row_data["red_motion_type"]
        ig_pictograph.arrows[BLUE].motion_type = pd_row_data["blue_motion_type"]
        ig_pictograph.motions[RED].motion_type = pd_row_data["red_motion_type"]
        ig_pictograph.motions[BLUE].motion_type = pd_row_data["blue_motion_type"]

        ig_pictograph.arrows[RED].motion = ig_pictograph.motions[RED]
        ig_pictograph.arrows[BLUE].motion = ig_pictograph.motions[BLUE]

        ig_pictograph.motions[RED].end_orientation = ig_pictograph.motions[
            RED
        ].get_end_orientation()
        ig_pictograph.motions[BLUE].end_orientation = ig_pictograph.motions[
            BLUE
        ].get_end_orientation()

        ig_pictograph.motions[RED].update_prop_orientation()
        ig_pictograph.motions[BLUE].update_prop_orientation()

        for arrow in ig_pictograph.arrows.values():
            arrow.set_is_svg_mirrored_from_attributes()
            arrow.update_mirror()
            arrow.update_appearance()

        for prop in ig_pictograph.props.values():
            prop.update_rotation()
            prop.update_appearance()

        motion = ig_pictograph.motions[arrow.color]
        arrow.motion, prop.motion = motion, motion
        arrow.ghost = ig_pictograph.ghost_arrows[arrow.color]
        arrow.ghost.motion = motion
        ig_pictograph.update_pictograph()
        return ig_pictograph
