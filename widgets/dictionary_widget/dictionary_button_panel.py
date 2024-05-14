from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QApplication, QMessageBox
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_preview_area import DictionaryPreviewArea


class DictionaryButtonPanel(QWidget):
    delete_variation_button: QPushButton
    delete_word_button: QPushButton
    edit_sequence_button: QPushButton

    def __init__(self, preview_area: "DictionaryPreviewArea"):
        super().__init__(preview_area)
        self.preview_area = preview_area
        self.dictionary_widget = preview_area.dictionary_widget
        self._setup_buttons()

    def _setup_buttons(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(10)

        # Define button data
        buttons_data = {
            "edit_sequence": {
                "icon": "edit.svg",
                "tooltip": "Edit Sequence",
                "action": self.edit_sequence,
            },
            "save_image": {
                "icon": "save_image.svg",
                "tooltip": "Save Image",
                "action": self.save_image,
            },
            "delete_variation": {
                "icon": "delete.svg",
                "tooltip": "Delete Variation",
                "action": self.delete_variation,
            },
            "delete_word": {
                "icon": "delete.svg",
                "tooltip": "Delete Word",
                "action": self.delete_word,
            },
        }

        # Create buttons based on the data defined
        for key, data in buttons_data.items():
            icon_path = get_images_and_data_path(
                f"images/icons/sequence_widget_icons/{data['icon']}"
            )
            button = QPushButton(QIcon(icon_path), "", self, toolTip=data["tooltip"])
            button.setToolTip(data["tooltip"])
            button.clicked.connect(data["action"])
            self.layout.addWidget(button)
            setattr(self, f"{key}_button", button)
            # set minimum size to be 1/10 of the dictionary widget width

            btn_size = int(self.dictionary_widget.width() // 10)
            icon_size = int(btn_size * 0.8)
            button.setMinimumSize(QSize(btn_size, btn_size))
            button.setMaximumSize(QSize(btn_size, btn_size))
            button.setIconSize(QSize(icon_size, icon_size))

    def edit_sequence(self):
        if not hasattr(self, "sequence_populator"):
            self.sequence_populator = self.dictionary_widget.sequence_populator
        if self.preview_area.sequence_json:
            self.preview_area.main_widget.setCurrentIndex(
                self.preview_area.main_widget.builder_tab_index
            )
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            self.sequence_populator.load_sequence_from_json(
                self.preview_area.sequence_json
            )
            QApplication.restoreOverrideCursor()
        else:
            QMessageBox.warning(
                self, "No Selection", "Please select a thumbnail first."
            )

    def save_image(self):
        QMessageBox.information(self, "Action", "Save Image Clicked")

    def delete_variation(self):
        QMessageBox.information(self, "Action", "Delete Variation Clicked")

    def delete_word(self):
        QMessageBox.information(self, "Action", "Delete Word Clicked")
