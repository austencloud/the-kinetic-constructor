from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QCheckBox, QLineEdit, QWidget

if TYPE_CHECKING:
    from widgets.image_export_dialog.image_export_dialog import ImageExportDialog


class ExportDialogControlPanel(QWidget):
    def __init__(self, export_dialog: "ImageExportDialog"):
        super().__init__()
        self.parent_dialog = export_dialog
        self.layout: QVBoxLayout = QVBoxLayout(self)

        self.include_start_pos_check = QCheckBox("Include Start Position", self)
        self.include_start_pos_check.setChecked(True)
        self.add_name_field = QLineEdit("Your Name", self)
        self.add_date_field = QLineEdit("Date", self)
        self.ok_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)

        self.layout.addWidget(self.include_start_pos_check)
        self.layout.addWidget(self.add_name_field)
        self.layout.addWidget(self.add_date_field)
        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(export_dialog.accept)
        self.cancel_button.clicked.connect(export_dialog.reject)
