from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from widgets.dictionary_widget.thumbnail_box.navigation_buttons_widget import (
    ThumbnailBoxNavButtonsWidget,
)
from widgets.dictionary_widget.thumbnail_box.preview_area_nav_buttons_widget import (
    PreviewAreaNavButtonsWidget,
)

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_widget import DictionaryWidget


class DictionaryPreviewArea(QWidget):
    def __init__(self, dictionary_widget: "DictionaryWidget"):
        super().__init__(dictionary_widget)
        self.layout = QVBoxLayout(self)
        self.image_label = QLabel(self)  # Assuming this is where the image is shown
        self.variation_number_label = QLabel("Variation 1", self)
        self.nav_buttons = PreviewAreaNavButtonsWidget(self)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.variation_number_label)
        self.layout.addWidget(self.nav_buttons)
        self.thumbnails = []
        self.main_widget = dictionary_widget.main_widget
        self.selected_thumbnail = None
        self.sequence_populator = dictionary_widget.sequence_populator
        self.update_thumbnails()

    def update_thumbnails(self, thumbnails=[]):
        self.thumbnails = thumbnails
        if self.thumbnails:
            self.nav_buttons.enable_buttons(True)
            self.update_preview(0)  # Start with the first thumbnail if available
        else:
            self.nav_buttons.enable_buttons(False)
            self.update_preview(None)  # No thumbnails available

    def update_preview(self, index):
        if self.thumbnails and index is not None:
            pixmap = QPixmap(self.thumbnails[index])
            self.image_label.setPixmap(
                pixmap.scaled(
                    self.image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            self.variation_number_label.setText(f"Variation {index + 1}")
        else:
            self.image_label.setText(
                "No image available"
            )  # Default text or action when no thumbnails exist

    def select_thumbnail(self, index):
        self.update_thumbnails(
            self.thumbnails
        )  # Assuming you fill this list based on selection
        self.update_preview(index)

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.edit_sequence_button)

    def _setup_buttons(self):
        self.edit_sequence_button = QPushButton("Edit Sequence")
        self.edit_sequence_button.clicked.connect(self.edit_sequence)

    def _setup_preview_image_label(self):
        default_text = "Select a sequence to display it here."
        self.image_label = QLabel(default_text)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

    def update_preview(self, index):
        if self.thumbnails and index is not None:
            pixmap = QPixmap(self.thumbnails[index])
            self.image_label.setPixmap(
                pixmap.scaled(
                    self.image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            self.variation_number_label.setText(f"Variation {index + 1}")
        else:
            self.image_label.setText("Select a sequence to display it here.")
            self.variation_number_label.setText("No Variation")

    def showEvent(self, event):
        font = self.image_label.font()
        font.setPointSizeF(self.main_widget.width() * 0.01)
        self.image_label.setFont(font)
        super().showEvent(event)
