# In PreferencesDialog.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton

if TYPE_CHECKING:
    from main import MainWindow


class PreferencesDialog(QDialog):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self.settings_manager = main_window.settings_manager
        self.scroll_area = (
            self.main_window.main_widget.main_tab_widget.codex.scroll_area
        )
        self.setWindowTitle("Preferences")
        self.setLayout(QVBoxLayout())

        self.column_count_label = QLabel("Column Count:")
        self.column_count_spinbox = QSpinBox()
        self.column_count_spinbox.setMinimum(1)  # Minimum number of columns
        self.column_count_spinbox.setMaximum(20)  # Maximum number of columns
        self.column_count_spinbox.setValue(
            self.scroll_area.display_manager.COLUMN_COUNT
        )
        self.column_count_spinbox.valueChanged.connect(self.update_column_count)

        self.layout().addWidget(self.column_count_label)
        self.layout().addWidget(self.column_count_spinbox)
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.close)
        self.layout().addWidget(self.apply_button)

        initial_column_count = self.settings_manager.get_setting("column_count")
        self.column_count_spinbox.setValue(initial_column_count)
        self.scroll_area.display_manager.COLUMN_COUNT = initial_column_count
        self.scroll_area.update_pictographs()

    def update_column_count(self, value) -> None:
        self.settings_manager.set_setting('column_count', value)
        self.scroll_area.display_manager.COLUMN_COUNT = value
        self.scroll_area.update_pictographs()

