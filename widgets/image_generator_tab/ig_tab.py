from typing import TYPE_CHECKING, Dict, List
import pandas as pd
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QFrame,
    QApplication,
)
from PyQt6.QtCore import Qt, pyqtSignal
from constants import END_POS, IG_PICTOGRAPH, LETTER, START_POS
from widgets.image_generator_tab.ig_filter_frame import IGFilterFrame
from widgets.image_generator_tab.ig_letter_button_frame import IGLetterButtonFrame
from widgets.image_generator_tab.ig_pictograph import IGPictograph
from widgets.image_generator_tab.ig_scroll import IGScrollArea


if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class IGTab(QWidget):
    imageGenerated = pyqtSignal(str)
    selected_letters: List[IGPictograph] = []

    ### INITIALIZATION ###

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.pictograph_df = self.load_and_sort_data("PictographDataFrame.csv")
        self._setup_ui()

    ### UI SETUP ###

    def _setup_ui(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setLayout(self.layout)
        self.setup_buttons()
        self.ig_scroll_area = IGScrollArea(self.main_widget, self)
        self.filter_frame = IGFilterFrame(self)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.left_layout.addWidget(self.filter_frame)
        self.left_layout.addWidget(self.ig_scroll_area)
        self.right_layout.addWidget(self.button_panel)
        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.right_layout)
        self.connect_buttons(self.letter_button_frame)

    def setup_buttons(self):
        self.letter_button_frame, self.action_button_frame = self.setup_button_frames()
        self.button_panel = self._setup_button_panel(
            self.letter_button_frame, self.action_button_frame
        )

    def connect_buttons(self, letter_button_frame):
        for key, button in letter_button_frame.buttons.items():
            button.clicked.connect(
                lambda checked, letter=key: self.on_letter_button_clicked(letter)
            )

    def setup_button_frames(self):
        letter_button_frame = IGLetterButtonFrame(self.main_widget)
        letter_button_frame.setStyleSheet("QFrame { border: 1px solid black; }")
        action_button_frame = self._setup_action_button_frame()
        return letter_button_frame, action_button_frame

    def _setup_button_panel(self, letter_button_frame, action_button_frame) -> QFrame:
        button_panel = QFrame()
        button_panel_layout = QVBoxLayout()
        button_panel.setLayout(button_panel_layout)
        button_panel.setStyleSheet("QFrame { border: 1px solid black; }")
        button_panel.setContentsMargins(0, 0, 0, 0)
        button_panel_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        button_panel_layout.setContentsMargins(0, 0, 0, 0)
        button_panel_layout.setSpacing(0)
        button_panel_layout.addWidget(letter_button_frame, 8)
        button_panel_layout.addWidget(action_button_frame, 1)
        self.button_panel_layout = button_panel_layout
        return button_panel

    def _setup_action_button_frame(self) -> QFrame:
        action_button_frame = QFrame()
        action_buttons = self._setup_action_buttons()
        action_button_frame_layout = QVBoxLayout(action_button_frame)
        action_button_frame_layout.setContentsMargins(0, 0, 0, 0)
        action_button_frame_layout.setSpacing(0)
        for button in action_buttons.values():
            action_button_frame_layout.addWidget(button)

        return action_button_frame

    def _setup_action_buttons(self) -> Dict[str, QPushButton]:
        buttons = {}
        generate_all_images_button = QPushButton("Generate All Images 🧨", self)
        generate_all_images_button.setStyleSheet("font-size: 16px;")

        generate_selected_images_button = QPushButton("Generate Selected Images", self)
        generate_selected_images_button.setStyleSheet("font-size: 16px;")

        generate_all_images_button.clicked.connect(self.generate_all_images)
        generate_selected_images_button.clicked.connect(self.generate_selected_images)

        buttons["generate_all_button"] = generate_all_images_button
        buttons["generate_selected_button"] = generate_selected_images_button
        return buttons

    ### DATA LOADING ###

    def load_and_sort_data(self, file_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            df.set_index([START_POS, END_POS], inplace=True)
            df.sort_index(inplace=True)
            return df
        except Exception as e:
            # Handle specific exceptions as needed
            print(f"Error loading data: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error

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

    ### IMAGE GENERATION ###

    def on_letter_button_clicked(self, letter) -> None:
        print(f"Button for letter {letter} clicked")
        button = self.letter_button_frame.buttons[letter]

        if letter in self.selected_letters:
            self.selected_letters.remove(letter)
            button.setFlat(False)  # This makes the button appear not pressed
            button.setStyleSheet(self.get_button_style(pressed=False))
        else:
            self.selected_letters.append(letter)
            button.setFlat(True)  # This makes the button appear pressed
            button.setStyleSheet(self.get_button_style(pressed=True))
        self.ig_scroll_area.update_pictographs()

    def on_letter_checkbox_state_changed(self, state, letter) -> None:
        print(f"Checkbox for letter {letter} state changed: {state}")
        if state and letter not in self.selected_letters:
            self.selected_letters.append(letter)
        elif not state and letter in self.selected_letters:
            self.selected_letters.remove(letter)
        self.ig_scroll_area.update_pictographs()

    def generate_selected_images(self) -> None:
        main_widget = self.parentWidget()
        main_widget.setEnabled(False)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.setMouseTracking(False)
        for letter in self.selected_letters:
            pictograph_dict_list = self.main_widget.letters[letter]
            for pictograph_dict in pictograph_dict_list:
                ig_pictograph: IGPictograph = self.ig_scroll_area._create_pictograph(
                    pictograph_dict, IG_PICTOGRAPH
                )
                ig_pictograph.render_and_cache_image()
        main_widget.setEnabled(True)
        QApplication.restoreOverrideCursor()
        self.setMouseTracking(True)

    def generate_all_images(self) -> None:
        main_widget = self.parentWidget()
        main_widget.setEnabled(False)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.setMouseTracking(False)
        for letter, pictograph_dict_list in self.main_widget.letters.items():
            for pictograph_dict in pictograph_dict_list:
                ig_pictograph: IGPictograph = self.ig_scroll_area._create_pictograph(
                    pictograph_dict, IG_PICTOGRAPH
                )
                ig_pictograph.render_and_cache_image()
        main_widget.setEnabled(True)
        QApplication.restoreOverrideCursor()
        self.setMouseTracking(True)

    def toggle_pictograph_selection(self, state, index) -> None:
        if state == Qt.CheckState.Checked:
            self.selected_letters.append(index)
        else:
            self.selected_letters.remove(index)
