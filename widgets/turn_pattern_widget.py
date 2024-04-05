import json
import os
import shutil
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QListWidgetItem,
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtGui import QFont
from path_helpers import get_images_and_data_path, get_user_editable_resource_path
from widgets.turn_pattern_converter import TurnPatternConverter

if TYPE_CHECKING:
    from widgets.main_builder_widget.builder_toolbar import (
        BuilderToolbar,
    )


class TurnPatternWidget(QWidget):
    def __init__(self, builder_toolbar: "BuilderToolbar") -> None:
        super().__init__()
        self.builder_toolbar = builder_toolbar
        self.main_widget = builder_toolbar.main_widget
        self.current_sequence_json_handler = (
            self.builder_toolbar.main_widget.json_manager.current_sequence_json_handler
        )
        self.turn_patterns_path = get_user_editable_resource_path("turn_patterns.json")
        self._setup_ui()
        self.ensure_turn_patterns_file_exists()
        self.load_turn_patterns()
        self.apply_button.clicked.connect(self.apply_turn_pattern)
        self.save_button.clicked.connect(self.save_turn_pattern)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.turn_pattern_list = QListWidget()
        self.apply_button = QPushButton("Apply Turn Pattern")
        self.save_button = QPushButton("Save Current Turn Pattern")

        # Increase font size for the widgets

        layout.addWidget(self.turn_pattern_list)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.save_button)
        self.turn_pattern_list.itemDoubleClicked.connect(self.apply_turn_pattern)

    def ensure_turn_patterns_file_exists(self):
        """
        Ensures that the turn_patterns.json file exists in the user's editable resource path.
        If the file does not exist, it is either copied from the bundled resources or initialized with an empty list.
        """
        user_editable_path = get_user_editable_resource_path("turn_patterns.json")
        if not os.path.exists(user_editable_path):
            bundled_path = get_images_and_data_path("turn_patterns.json")
            if os.path.exists(bundled_path):
                shutil.copy(bundled_path, user_editable_path)
            else:
                with open(user_editable_path, "w") as file:
                    json.dump([], file)

    def load_turn_patterns(self) -> None:
        try:
            with open(self.turn_patterns_path, "r") as file:
                patterns = json.load(file)
                self.turn_pattern_list.clear()
                for pattern_dict in patterns:
                    for name, pattern in pattern_dict.items():
                        item = QListWidgetItem(f"{name}: {pattern}")
                        item.setData(Qt.ItemDataRole.UserRole, pattern)
                        self.turn_pattern_list.addItem(item)
        except FileNotFoundError:
            print("Turn patterns file not found. Starting with an empty list.")

    def save_turn_pattern(self) -> None:
        current_pattern = self.get_current_turn_pattern()
        pattern_name, ok = QInputDialog.getText(
            self, "Save Pattern", "Enter pattern name:"
        )
        if ok:
            if not pattern_name:
                pattern_name = "Pattern " + str(self.turn_pattern_list.count() + 1)

            new_pattern = {pattern_name: current_pattern}

            patterns = []
            try:
                with open(self.turn_patterns_path, "r") as file:
                    patterns = json.load(file)
            except FileNotFoundError:
                pass

            patterns.append(new_pattern)

            with open(self.turn_patterns_path, "w") as file:
                json.dump(patterns, file, indent=4)

            self.load_turn_patterns()

    def get_current_turn_pattern(self) -> str:
        sequence = self.current_sequence_json_handler.load_current_sequence_json()
        pattern = TurnPatternConverter.sequence_to_pattern(sequence)
        return pattern

    def apply_turn_pattern(self) -> None:
        selected_items = self.turn_pattern_list.selectedItems()
        if not selected_items:
            return
        pattern_str = selected_items[0].data(Qt.ItemDataRole.UserRole)
        self.current_sequence_json_handler.apply_turn_pattern_to_current_sequence(
            TurnPatternConverter.pattern_to_sequence(pattern_str)
        )

    def _set_font_size(self):
        font = QFont()
        font_size = self.builder_toolbar.width() // 55
        font.setPointSize(font_size)
        self.turn_pattern_list.setFont(font)
        self.apply_button.setFont(font)
        self.save_button.setFont(font)

    def resize_turn_pattern_widget(self) -> None:
        self._set_font_size()
