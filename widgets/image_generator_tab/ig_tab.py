import os
from typing import TYPE_CHECKING, Dict
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
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPainter
from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from widgets.image_generator_tab.ig_letter_button_frame import IGLetterButtonFrame
from widgets.image_generator_tab.ig_pictograph import IGPictograph
from widgets.image_generator_tab.ig_scroll import IGScroll

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


class IGTab(QWidget):
    imageGenerated = pyqtSignal(str)  # Signal to indicate when an image is generated

    ### INITIALIZATION ###

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.main_pictograph = (
            self.main_widget.graph_editor_tab.graph_editor.main_pictograph
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
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setLayout(self.layout)
        button_frame = QFrame()
        button_frame_layout = QVBoxLayout()
        letter_button_frame = IGLetterButtonFrame(self.main_widget, self)
        action_button_frame = QFrame()
        self.ig_scroll_area = IGScroll(self.main_widget, self)
        letter_button_frame.setStyleSheet(
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
        self.layout.addWidget(letter_button_frame)

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
        button_frame_layout.addWidget(letter_button_frame, 8)
        button_frame_layout.addWidget(action_button_frame, 1)
        self.layout.addWidget(self.ig_scroll_area)
        self.layout.addWidget(button_frame)
        letters = self.get_letters()
        letters.sort(
            key=lambda x: x
            if x not in ["Σ", "Δ", "θ", "Ω", "Φ", "Ψ", "Λ", "α", "β", "Γ"]
            else chr(ord(x) + 1000)
        )

        for key, button in letter_button_frame.buttons.items():
            button.clicked.connect(
                lambda checked, letter=key: self.on_letter_button_clicked(letter)
            )

    ### LETTERS ###

    def get_letters(self) -> List[str]:
        return self.pictograph_df.iloc[:, 0].unique().tolist()

    ### IMAGE GENERATION ###

    def on_letter_button_clicked(self, letter) -> None:
        print(f"Button for letter {letter} clicked")
        if letter in self.selected_pictographs:
            self.selected_pictographs.remove(letter)
        else:
            self.selected_pictographs.append(letter)
        self.ig_scroll_area.update_displayed_pictographs()

    def on_letter_checkbox_state_changed(self, state, letter) -> None:
        print(f"Checkbox for letter {letter} state changed: {state}")
        if state and letter not in self.selected_pictographs:
            self.selected_pictographs.append(letter)
        elif not state and letter in self.selected_pictographs:
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
        for index, pictograph_data in pictographs_for_letter.iterrows():
            # Updated to use actual pictograph data
            # checkbox_text = f"{pictograph_data['letter']}_"
            # checkbox = QCheckBox(checkbox_text)
            # checkbox.stateChanged.connect(
            #     lambda state, idx=index: self.toggle_pictograph_selection(state, idx)
            # )
            self.render_pictograph_to_image(pictograph_data)

    def toggle_pictograph_selection(self, state, index) -> None:
        if state == Qt.CheckState.Checked:
            self.selected_pictographs.append(index)
        else:
            self.selected_pictographs.remove(index)

    def render_pictograph_to_image(self, pictograph_data) -> None:
        # Create an IG_Pictograph instance from the pictograph data
        ig_pictograph = self._create_ig_pictograph_from_pictograph_data(pictograph_data)
        # Render scene to QImage
        image = QImage(
            int(ig_pictograph.width()),
            int(ig_pictograph.height()),
            QImage.Format.Format_ARGB32,
        )
        painter = QPainter(image)
        ig_pictograph.render(painter)
        painter.end()

        # Save image to file
        image_path = self.get_image_path(pictograph_data)
        image.save(image_path)
        self.imageGenerated.emit(image_path)

    ### OPTION CREATION ###

    def _create_ig_pictograph_from_pictograph_data(
        self, pictograph_data
    ) -> IGPictograph:
        ig_pictograph = IGPictograph(self.main_widget, self.ig_scroll_area)
        ig_pictograph.setSceneRect(0, 0, 750, 900)

        # Use the existing method to create motion dictionaries
        motion_dicts = [
            self._create_motion_dict(pictograph_data, color)
            for color in ["blue", "red"]
        ]

        # Add motions, arrows, and props to the IG_Pictograph instance
        for motion_dict in motion_dicts:
            self._add_motion_to_ig_pictograph(ig_pictograph, motion_dict)
            self._finalize_ig_pictograph_setup(ig_pictograph, motion_dict)

        ig_pictograph.view.resize_ig_pictograph()
        ig_pictograph.update_pictograph()

        return ig_pictograph

    def _create_arrow(self, ig_pictograph: "IGPictograph", motion_dict: Dict) -> Arrow:
        arrow_dict = {
            COLOR: motion_dict[COLOR],
            MOTION_TYPE: motion_dict[MOTION_TYPE],
            TURNS: motion_dict[TURNS],
        }
        arrow = Arrow(
            ig_pictograph, arrow_dict, ig_pictograph.motions[motion_dict[COLOR]]
        )
        ig_pictograph.arrows[arrow.color] = arrow
        arrow.motion = ig_pictograph.motions[arrow.color]
        ig_pictograph.addItem(arrow)
        return arrow

    def _create_prop(self, ig_pictograph: "IGPictograph", motion_dict: Dict) -> Prop:
        prop_dict = {
            COLOR: motion_dict[COLOR],
            PROP_TYPE: self.main_pictograph.prop_type,
            LOCATION: motion_dict[END_LOCATION],
            LAYER: 1,
            ORIENTATION: IN,
        }
        prop = Prop(ig_pictograph, prop_dict, ig_pictograph.motions[motion_dict[COLOR]])
        ig_pictograph.props[prop.color] = prop
        prop.motion = ig_pictograph.motions[prop.color]
        ig_pictograph.addItem(prop)
        return prop

    def _finalize_ig_pictograph_setup(
        self, ig_pictograph: "IGPictograph", motion_dict
    ) -> None:
        for motion in ig_pictograph.motions.values():
            if motion.color == motion_dict[COLOR]:
                motion.setup_attributes(motion_dict)
                motion.arrow = ig_pictograph.arrows[motion.color]
                motion.prop = ig_pictograph.props[motion.color]
                motion.assign_location_to_arrow()
                motion.update_prop_orientation_and_layer()
                motion.arrow.set_is_svg_mirrored_from_attributes()
                motion.arrow.update_mirror()
                motion.arrow.update_appearance()
                motion.prop.update_appearance()
                motion.arrow.motion = motion
                motion.prop.motion = motion
                motion.arrow.ghost = ig_pictograph.ghost_arrows[motion.color]
                motion.arrow.ghost.motion = motion
                motion.arrow.ghost.set_is_svg_mirrored_from_attributes()
                motion.arrow.ghost.update_appearance()
                motion.arrow.ghost.update_mirror()
        ig_pictograph.update_pictograph()

    @staticmethod
    def _setup_motion_relations(
        ig_pictograph: IGPictograph, arrow: Arrow, prop: Prop
    ) -> None:
        motion = ig_pictograph.motions[arrow.color]
        arrow.motion, prop.motion = motion, motion
        arrow.ghost = ig_pictograph.ghost_arrows[arrow.color]
        arrow.ghost.motion = motion

    def _add_motion_to_ig_pictograph(
        self, ig_pictograph: "IGPictograph", motion_dict: Dict
    ) -> None:
        arrow = self._create_arrow(ig_pictograph, motion_dict)
        prop = self._create_prop(ig_pictograph, motion_dict)
        self._setup_motion_relations(ig_pictograph, arrow, prop)

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
