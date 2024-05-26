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
from PyQt6.QtCore import pyqtSignal
from datetime import datetime

if TYPE_CHECKING:
    from widgets.image_export_dialog.image_export_dialog import ImageExportDialog


class ExportDialogControlPanel(QWidget):
    optionChanged = pyqtSignal()

    def __init__(self, export_dialog: "ImageExportDialog"):
        super().__init__()
        self.export_dialog = export_dialog
        self.settings_manager = export_dialog.export_manager.settings_manager
        self.layout: QVBoxLayout = QVBoxLayout(self)

        self.include_start_pos_check = QCheckBox("Include Start Position", self)
        self.include_start_pos_check.setChecked(True)
        self.include_start_pos_check.toggled.connect(self.optionChanged.emit)

        self.user_layout = QHBoxLayout()
        self.user_combo_box = QComboBox(self)
        self.add_user_button = QPushButton("Add User", self)
        self.user_layout.addWidget(self.user_combo_box, 6)
        self.user_layout.addWidget(self.add_user_button, 1)

        self.add_date_field = QLineEdit(self)
        self._set_current_date()
        self._populate_user_profiles()

        self._setup_buttons()

        self.layout.addStretch(1)
        self.layout.addWidget(self.include_start_pos_check)
        self.layout.addLayout(self.user_layout)
        self.layout.addWidget(self.add_date_field)
        self.layout.addLayout(self.button_layout)
        self.layout.addStretch(1)

        self.ok_button.clicked.connect(self._save_settings_and_accept)
        self.cancel_button.clicked.connect(export_dialog.reject)
        self.add_user_button.clicked.connect(self._add_new_user)

        self.optionChanged.connect(self.update_preview_based_on_options)
        self.include_start_pos_check.setChecked(
            self.export_dialog.export_manager.include_start_pos
        )
        self.include_start_pos_check.toggled.connect(
            self.export_dialog.update_export_setting_and_layout
        )

    def _setup_buttons(self):
        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.ok_button)

    def _set_current_date(self):
        current_date = datetime.now().strftime("%m-%d-%Y")
        self.add_date_field.setText(current_date)

    def _populate_user_profiles(self):
        user_profiles = self.settings_manager.get_image_export_setting(
            "user_profiles", {}
        )
        current_user = self.settings_manager.get_image_export_setting(
            "current_user", "Your Name"
        )
        for user_name in user_profiles.keys():
            self.user_combo_box.addItem(user_name)
        if current_user in user_profiles:
            index = self.user_combo_box.findText(current_user)
            if index != -1:
                self.user_combo_box.setCurrentIndex(index)
        self.user_combo_box.currentIndexChanged.connect(self._update_current_user)

    def _update_current_user(self):
        selected_user = self.user_combo_box.currentText()
        if selected_user:
            self.settings_manager.set_image_export_setting(
                "current_user", selected_user
            )

    def _add_new_user(self):
        text, ok = QInputDialog.getText(self, "Add New User", "Enter user name:")
        if ok and text:
            new_user_profile = {"name": text, "export_date": self.add_date_field.text()}
            self.settings_manager.add_or_update_user_profile(new_user_profile)
            self.user_combo_box.addItem(text)
            self.user_combo_box.setCurrentText(text)

    def _save_settings_and_accept(self):
        current_user = self.user_combo_box.currentText()
        current_date = self.add_date_field.text()
        user_profile = {"name": current_user, "export_date": current_date}
        self.settings_manager.add_or_update_user_profile(user_profile)
        self.export_dialog.accept()

    def update_preview_based_on_options(self):
        include_start_pos = self.include_start_pos_check.isChecked()
        self.export_dialog.preview_panel.update_preview_with_start_pos(
            include_start_pos, self.export_dialog.sequence
        )
