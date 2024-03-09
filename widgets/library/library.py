from PyQt6.QtWidgets import QTreeView, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir, QModelIndex, Qt
import json
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class Library(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.setup_ui()
        self.main_widget = main_widget

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        self.setup_tree_view(layout)
        self.setup_preview_area(layout)
        self.setLayout(layout)

    def setup_tree_view(self, layout: QVBoxLayout) -> None:
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath() + "/library")

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.currentPath() + "/library"))
        self.tree_view.doubleClicked.connect(self.on_double_clicked)
        layout.addWidget(self.tree_view)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)

    def setup_preview_area(self, layout: QVBoxLayout) -> None:
        self.preview_area = QWidget()
        self.preview_area.setStyleSheet("background-color: gray;")
        layout.addWidget(self.preview_area)

    def on_double_clicked(self, index: QModelIndex) -> None:
        file_path = self.model.filePath(index)
        if file_path.endswith(".json"):
            self.load_sequence_from_file(file_path)
        else:
            QMessageBox.information(
                self, "Information", "Selected file is not a JSON sequence file."
            )

    def load_sequence_from_file(self, file_path) -> None:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                sequence_data: list[dict[str, str]] = json.load(file)
            self.populate_sequence(sequence_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load sequence: {str(e)}")

    def populate_sequence(self, sequence_data: list[dict[str, str]]) -> None:
        if not sequence_data:
            return
        json_handler = self.main_widget.json_manager.current_sequence_json_handler
        start_pos_view = self.main_widget.sequence_widget.beat_frame.start_pos_view
        start_pos_manager = (
            self.main_widget.main_tab_widget.sequence_constructor.start_position_picker.start_pos_manager
        )
        sequence_widget = self.main_widget.sequence_widget
        sequence_widget.button_frame.clear_sequence(
            show_indicator=False, should_reset_to_start_pos_picker=False
        )

        start_pos_beat = start_pos_manager._convert_current_sequence_json_entry_to_start_pos_pictograph(
            sequence_data
        )
        json_handler.set_start_position_data(start_pos_beat)
        start_pos_view.set_start_pos_beat(start_pos_beat)

        for pictograph_dict in sequence_data:
            if pictograph_dict.get("sequence_start_position"):
                continue
            sequence_widget.populate_sequence(pictograph_dict)

        sequence_builder = self.main_widget.main_tab_widget.sequence_constructor
        last_beat = sequence_widget.beat_frame.get_last_filled_beat().beat
        sequence_builder.current_pictograph = last_beat

        if sequence_builder.start_position_picker.isVisible():
            sequence_builder.transition_to_sequence_building()

        sequence_builder.option_picker.scroll_area._add_and_display_relevant_pictographs(
            sequence_builder.option_picker.option_manager.get_next_options()
        )
