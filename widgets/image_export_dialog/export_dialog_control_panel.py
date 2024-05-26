from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QCheckBox,
    QLineEdit,
    QWidget,
    QHBoxLayout,
    QComboBox,
    QInputDialog,
)
from PyQt6.QtCore import pyqtSignal, Qt
from datetime import datetime

if TYPE_CHECKING:
    from widgets.image_export_dialog.image_export_dialog import ImageExportDialog


class ExportDialogControlPanel(QWidget):
    optionChanged = pyqtSignal()

    def __init__(self, export_dialog: "ImageExportDialog"):
        super().__init__()
        self.export_dialog = export_dialog
        self.settings_manager = export_dialog.export_manager.settings_manager
        self.user_combo_box = self.settings_manager.user_manager.user_combo_box

        self._setup_checkboxes()
        self._setup_fields()
        self._setup_buttons()
        self._setup_layout()
        self._connect_signals()

    def _setup_layout(self):
        """Setup the layout of the control panel."""
        self.user_input_layout = QHBoxLayout()
        self.user_input_layout.addWidget(self.add_user_button, 1)
        self.user_input_layout.addWidget(self.user_combo_box, 2)
        self.user_input_layout.addWidget(self.add_notes_field, 5)
        self.user_input_layout.addWidget(self.add_date_field, 2)

        self.checkbox_layout = QHBoxLayout()
        self.checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.checkbox_layout.addWidget(self.include_start_pos_check)
        self.checkbox_layout.addWidget(self.add_info_check)

        self.open_dir_layout = QHBoxLayout()
        self.open_dir_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.open_dir_layout.addWidget(self.open_directory_check)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.addLayout(self.checkbox_layout)
        self.layout.addLayout(self.open_dir_layout)
        self.layout.addLayout(self.user_input_layout)

    def _connect_signals(self):
        """Connect signals to their respective slots."""
        self.optionChanged.connect(lambda: self.update_preview_based_on_options())
        self.include_start_pos_check.toggled.connect(
            self.export_dialog.update_export_setting_and_layout
        )

    def _setup_checkboxes(self):
        """Setup the checkboxes for the control panel."""
        self.include_start_pos_check = QCheckBox("Add Start Position", self)
        self.include_start_pos_check.setChecked(
            self.settings_manager.get_image_export_setting(
                "include_start_position", True
            )
        )
        self.include_start_pos_check.toggled.connect(self.optionChanged.emit)

        self.add_info_check = QCheckBox("Add Info", self)
        self.add_info_check.setChecked(
            self.settings_manager.get_image_export_setting("add_info", True)
        )
        self.add_info_check.toggled.connect(self.toggle_add_info)

        self.open_directory_check = QCheckBox("Open file location after export", self)
        self.open_directory_check.setChecked(
            self.settings_manager.get_image_export_setting(
                "open_directory_on_export", True
            )
        )
        self.open_directory_check.toggled.connect(self.update_open_directory_setting)

    def _setup_buttons(self):
        """Setup the buttons for the control panel."""
        self.add_user_button = QPushButton("Add User", self)
        self.add_user_button.clicked.connect(
            self.settings_manager.user_manager.add_new_user
        )

    def _setup_fields(self):
        """Setup the input fields for the control panel."""
        self.add_notes_field = QLineEdit(self)
        default_note = "Created using The Kinetic Alphabet"
        self.add_notes_field.setText(default_note)

        self.add_date_field = QLineEdit(self)
        current_date = datetime.now().strftime("%m-%d-%Y")
        current_date = "-".join([str(int(part)) for part in current_date.split("-")])
        self.add_date_field.setText(current_date)

    def save_settings_and_accept(self):
        """Save the current settings and accept the dialog."""
        current_user = self.user_combo_box.currentText()
        current_date = self.add_date_field.text()
        user_profile = {"name": current_user, "export_date": current_date}
        self.settings_manager.add_or_update_user_profile(user_profile)
        self.export_dialog.accept()

    def update_open_directory_setting(self):
        """Update the setting for opening the directory after export."""
        self.settings_manager.set_image_export_setting(
            "open_directory_on_export", self.open_directory_check.isChecked()
        )

    def update_preview_based_on_options(self):
        """Update the preview panel based on the current options."""
        include_start_pos = self.include_start_pos_check.isChecked()
        add_info = self.add_info_check.isChecked()
        self.export_dialog.preview_panel.update_preview_with_start_pos(
            include_start_pos, add_info, self.export_dialog.sequence
        )

    def toggle_add_info(self):
        """Toggle the state of the additional info fields based on the checkbox."""
        state = self.add_info_check.isChecked()
        self.user_combo_box.setEnabled(state)
        self.add_user_button.setEnabled(state)
        self.add_date_field.setEnabled(state)
        self.add_notes_field.setEnabled(state)
        color = "gray" if not state else ""
        self.add_date_field.setStyleSheet(f"color: {color};")
        self.user_combo_box.setStyleSheet(f"color: {color};")
        self.add_user_button.setStyleSheet(f"color: {color};")
        self.add_notes_field.setStyleSheet(f"color: {color};")
        self.export_dialog.update_preview_based_on_options()
        self.settings_manager.set_image_export_setting("add_info", state)
