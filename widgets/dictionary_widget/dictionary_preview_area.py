from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox
from widgets.dictionary_widget.thumbnail_box.thumbnail_box_nav_buttons_widget import (
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
        self.image_label = QLabel(self)
        self.variation_number_label = QLabel("Variation 1", self)
        self.nav_buttons = PreviewAreaNavButtonsWidget(self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.variation_number_label)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.nav_buttons)
        self.layout.addStretch(1)
        self.variation_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._setup_buttons()
        self.thumbnails = []
        self.main_widget = dictionary_widget.main_widget
        self.selected_thumbnail = None
        self.current_thumbnail_box: ThumbnailBox = None
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
            # Load the pixmap from the thumbnail path
            pixmap = QPixmap(self.thumbnails[index])

            # Get the width of the image_label widget (which should match the width of the preview area)
            label_width = self.image_label.width()

            # Calculate the new height maintaining the aspect ratio
            aspect_ratio = pixmap.height() / pixmap.width()
            new_height = int(label_width * aspect_ratio)

            # Set the pixmap with the new size
            scaled_pixmap = pixmap.scaled(
                label_width,
                new_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.image_label.setPixmap(scaled_pixmap)

            # Update the variation number label
            self.variation_number_label.setText(f"Variation {index + 1}")
        else:
            # Default text when there is no image available
            self.image_label.setText("No image available")
            self.variation_number_label.setText("No Variation")

    def select_thumbnail(self, thumbnail_box, index):
        self.update_thumbnails(self.thumbnails)
        self.update_preview(index)
        self.current_thumbnail_box = thumbnail_box

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

    def showEvent(self, event):
        font = self.image_label.font()
        font.setPointSizeF(self.main_widget.width() * 0.01)
        self.image_label.setFont(font)
        super().showEvent(event)
