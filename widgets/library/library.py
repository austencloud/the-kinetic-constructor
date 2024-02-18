from PyQt6.QtWidgets import QTreeView, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir, QModelIndex, Qt
import json
from typing import TYPE_CHECKING
from widgets.pictograph.pictograph import Pictograph
from widgets.sequence_widget.sequence_beat_frame.start_pos_beat import StartPositionBeat
from Enums.letters import Letter

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class Library(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.setup_tree_view(layout)
        self.setup_preview_area(layout)
        self.setLayout(layout)

    def setup_tree_view(self, layout: QVBoxLayout):
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath() + "/library")

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.currentPath() + "/library"))
        self.tree_view.doubleClicked.connect(self.on_double_clicked)
        layout.addWidget(self.tree_view)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)

    def setup_preview_area(self, layout: QVBoxLayout):
        self.preview_area = QWidget()
        self.preview_area.setStyleSheet("background-color: gray;")
        layout.addWidget(self.preview_area)

    def on_double_clicked(self, index: QModelIndex):
        file_path = self.model.filePath(index)
        if file_path.endswith(".json"):
            self.load_sequence_from_file(file_path)
        else:
            QMessageBox.information(
                self, "Information", "Selected file is not a JSON sequence file."
            )

    def load_sequence_from_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                sequence_data: list[dict[str, str]] = json.load(file)
            self.populate_sequence(sequence_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load sequence: {str(e)}")

    def populate_sequence(self, sequence_data: list[dict[str, str]]):
        if not sequence_data:
            return
        json_handler = self.main_widget.json_manager.current_sequence_json_handler
        start_pos_view = self.main_widget.sequence_widget.beat_frame.start_pos_view

        sequence_widget = self.main_widget.sequence_widget
        sequence_widget.button_frame.clear_sequence(show_indicator=False)

        start_pos_beat = self._convert_pictograph_to_start_pos_beat(sequence_data)
        json_handler.set_start_position_data(start_pos_beat)
        start_pos_view.set_start_pos_beat(start_pos_beat)

        for pictograph_dict in sequence_data:
            if pictograph_dict.get("sequence_start_position"):
                continue
            sequence_widget.populate_sequence(pictograph_dict)

        sequence_builder = self.main_widget.main_tab_widget.sequence_builder
        last_beat = sequence_widget.beat_frame.get_last_filled_beat().beat
        sequence_builder.current_pictograph = last_beat
        sequence_builder.option_picker.scroll_area._add_and_display_relevant_pictographs(
            sequence_builder.option_picker.option_manager.get_next_options()
        )
        sequence_builder.transition_to_sequence_building()

    def _convert_pictograph_to_start_pos_beat(self, sequence_data):
        start_position_pictograph = self.get_start_pos_pictograph(
            sequence_data[0] if sequence_data else None
        )
        start_pos_beat = StartPositionBeat(
            self.main_widget, self.main_widget.sequence_widget.beat_frame
        )
        start_pos_beat.updater.update_pictograph(
            start_position_pictograph.pictograph_dict
        )

        return start_pos_beat

    def get_start_pos_pictograph(self, start_pos_data) -> "Pictograph":
        if not start_pos_data:
            return None
        start_pos_key = start_pos_data["end_pos"]
        letter_str = self.start_pos_key_to_letter(start_pos_key)
        letter = Letter(letter_str)
        matching_letter_pictographs = self.main_widget.letters.get(letter, [])
        for pictograph_dict in matching_letter_pictographs:
            if pictograph_dict["start_pos"] == start_pos_key:

                pictograph_dict["blue_start_ori"] = start_pos_data["blue_end_ori"]
                pictograph_dict["red_start_ori"] = start_pos_data["red_end_ori"]
                pictograph_dict["blue_end_ori"] = start_pos_data["blue_end_ori"]
                pictograph_dict["red_end_ori"] = start_pos_data["red_end_ori"]

                pictograph_factory = self.main_widget.sequence_widget.pictograph_factory
                pictograph_key = pictograph_factory.generate_pictograph_key_from_dict(
                    pictograph_dict
                )
                return pictograph_factory.get_or_create_pictograph(
                    pictograph_key, pictograph_dict
                )

        print(f"No matching start position found for key: {start_pos_key}")
        return None

    def start_pos_key_to_letter(self, start_pos_key: str):
        mapping = {"alpha": "α", "beta": "β", "gamma": "Γ"}
        for key in mapping:
            if start_pos_key.startswith(key):
                return mapping[key]
        return None
