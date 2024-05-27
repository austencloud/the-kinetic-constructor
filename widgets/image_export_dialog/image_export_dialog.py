from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PyQt6.QtCore import Qt

from widgets.image_export_dialog.export_dialog_control_panel import (
    ExportDialogControlPanel,
)
from widgets.image_export_dialog.export_dialog_preview_panel import (
    ExportDialogPreviewPanel,
)

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.sequence_image_export_manager import (
        SequenceImageExportManager,
    )


class ImageExportDialog(QDialog):
    def __init__(
        self, export_manager: "SequenceImageExportManager", sequence: list[dict]
    ):
        super().__init__(export_manager.main_widget)
        self.export_manager = export_manager
        self.sequence = sequence
        self.main_widget = export_manager.main_widget
        self.settings_manager = export_manager.settings_manager
        self.setWindowTitle("Save Image")
        self.setModal(True)
        self._resize_image_export_dialog()
        self._setup_components()
        self._setup_layout()
        self.update_preview_based_on_options()

    def _setup_open_directory_checkbox(self):
        self.open_directory_check = QCheckBox("Open file location after export", self)
        self.open_directory_check.setChecked(
            self.settings_manager.get_image_export_setting(
                "open_directory_on_export", True
            )
        )
        self.open_directory_check.toggled.connect(self.update_open_directory_setting)
        self.open_dir_layout = QHBoxLayout()
        self.open_dir_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.open_dir_layout.addWidget(self.open_directory_check)

    def update_open_directory_setting(self):
        """Update the setting for opening the directory after export."""
        self.settings_manager.set_image_export_setting(
            "open_directory_on_export", self.open_directory_check.isChecked()
        )

    def _setup_okay_cancel_buttons(self):
        self.ok_button = QPushButton("Save", self)
        self.ok_button.clicked.connect(self.control_panel.save_settings_and_accept)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.control_panel.export_dialog.reject)

    def _resize_image_export_dialog(self):
        main_width = self.main_widget.width()
        main_height = self.main_widget.height()
        self.resize(main_width // 3, int(main_height // 1.5))

    def _setup_components(self):
        self.preview_panel = ExportDialogPreviewPanel(self)
        self.control_panel = ExportDialogControlPanel(self)
        self._setup_okay_cancel_buttons()
        self._setup_open_directory_checkbox()

    def _setup_layout(self):
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.ok_button)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.preview_panel, 12)
        self.layout.addWidget(self.control_panel, 1)
        self.layout.addLayout(self.open_dir_layout, 1)
        self.layout.addLayout(self.button_layout, 1)

    def update_export_setting_and_layout(self):
        new_value = self.control_panel.include_start_pos_check.isChecked()
        self.export_manager.include_start_pos = new_value
        self.export_manager.settings_manager.set_image_export_setting(
            "include_start_position", new_value
        )
        self.update_preview_based_on_options()

    def get_export_options(self):
        return {
            "include_start_position": self.control_panel.include_start_pos_check.isChecked(),
            "add_info": self.control_panel.add_info_check.isChecked(),
            "user_name": self.control_panel.user_combo_box.currentText(),
            "export_date": self.control_panel.add_date_field.text(),
            "open_directory": self.open_directory_check.isChecked(),
        }

    def update_preview_based_on_options(self):
        include_start_pos = self.control_panel.include_start_pos_check.isChecked()
        options = self.get_export_options()
        self.preview_panel.update_preview_with_options(
            include_start_pos, self.sequence, options
        )

    def showEvent(self, event):
        super().showEvent(event)
        self.preview_panel.update_preview()
