from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_widget import DictionaryWidget


class DictionaryPreviewArea(QWidget):
    def __init__(self, dictionary_widget: "DictionaryWidget") -> None:
        super().__init__(dictionary_widget)
        self.main_widget = dictionary_widget.main_widget
        self.sequence_populator = dictionary_widget.sequence_populator
        self.selected_thumbnail = None

        self._setup_preview_label()
        self._setup_buttons()
        self._setup_layout()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.preview_label)
        self.layout.addWidget(self.edit_sequence_button)

    def _setup_buttons(self):
        self.edit_sequence_button = QPushButton("Edit Sequence")
        self.edit_sequence_button.clicked.connect(self.edit_sequence)

    def _setup_preview_label(self):
        self.preview_label = QLabel("Select a sequence to display it here.")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def edit_sequence(self):
        if self.selected_thumbnail:
            self.main_widget.setCurrentIndex(self.main_widget.builder_tab_index)
            self.sequence_populator.load_sequence_from_thumbnail(
                self.selected_thumbnail
            )

        else:
            QMessageBox.warning(
                self, "No Selection", "Please select a thumbnail first."
            )

    def update_preview(self, thumbnail_path: str):
        pixmap = QPixmap(thumbnail_path)
        self.preview_label.setPixmap(
            pixmap.scaled(
                self.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

    def showEvent(self, event):
        font = self.preview_label.font()
        font.setPointSizeF(self.main_widget.width() * 0.01)
        self.preview_label.setFont(font)
        super().showEvent(event)
