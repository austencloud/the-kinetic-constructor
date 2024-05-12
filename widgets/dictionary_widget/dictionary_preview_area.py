import os
import shutil
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QApplication,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QResizeEvent

from path_helpers import get_images_and_data_path
from preview_area_image_label import PreviewAreaImageLabel
from widgets.dictionary_widget.thumbnail_box.base_word_label import BaseWordLabel
from widgets.dictionary_widget.thumbnail_box.preview_area_nav_btns import (
    PreviewAreaNavButtonsWidget,
)
from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox

from widgets.dictionary_widget.thumbnail_box.thumbnail_image_label import (
    ThumbnailImageLabel,
)
from widgets.dictionary_widget.thumbnail_box.variation_number_label import (
    VariationNumberLabel,
)

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_widget import DictionaryWidget


class DictionaryPreviewArea(QWidget):
    def __init__(self, dictionary_widget: "DictionaryWidget"):
        super().__init__(dictionary_widget)
        self.thumbnails = []
        self.current_index = 0
        self.main_widget = dictionary_widget.main_widget
        self.dictionary_widget = dictionary_widget
        self.sequence_json = None
        self.current_thumbnail_box: ThumbnailBox = None
        self.base_word = ""
        self._setup_components()
        self.image_label.setStyleSheet("font: 20pt Arial; font-weight: bold;")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.variation_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_thumbnails()
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.base_word_label)
        self.layout.addWidget(self.variation_number_label)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.nav_buttons_widget)
        self.layout.addWidget(self.edit_sequence_button)
        self.layout.addWidget(self.delete_variation_button)
        self.layout.addWidget(self.delete_word_button)
        self.layout.addStretch(1)
        self.base_word_label.setFont(QFont("Arial", 30, QFont.Weight.Bold))

    def _setup_components(self):
        self.variation_number_label = VariationNumberLabel(self)
        self.base_word_label = BaseWordLabel(self.base_word)
        self.image_label = PreviewAreaImageLabel(self)
        self.nav_buttons_widget = PreviewAreaNavButtonsWidget(self)
        self.edit_sequence_button = QPushButton("Edit Sequence")
        self.edit_sequence_button.clicked.connect(self.edit_sequence)
        self.image_label.setText("Select a sequence to display it here.")
        self._setup_deletion_buttons()

    def _setup_deletion_buttons(self):
        self.delete_variation_button = QPushButton("Delete Variation", self)
        self.delete_variation_button.clicked.connect(
            self.dictionary_widget.deletion_manager.confirm_delete_variation
        )
        self.delete_word_button = QPushButton("Delete Base Word", self)
        self.delete_word_button.clicked.connect(
            self.dictionary_widget.deletion_manager.confirm_delete_word
        )

    def update_thumbnails(self, thumbnails=[]):
        self.thumbnails = thumbnails
        self.current_index = 0
        self.nav_buttons_widget.refresh()

        if self.thumbnails:
            self._show_buttons_and_labels()

        if len(self.thumbnails) > 1:
            self.nav_buttons_widget.show()
        elif not self.thumbnails:
            self._hide_buttons_and_labels()
            self.update_preview(None)

    def _show_buttons_and_labels(self):
        self.base_word_label.show()
        self.nav_buttons_widget.show()
        self.delete_word_button.show()
        self.delete_variation_button.show()
        self.edit_sequence_button.show()

    def _hide_buttons_and_labels(self):
        self.base_word_label.hide()
        self.nav_buttons_widget.hide()
        self.delete_word_button.hide()
        self.delete_variation_button.hide()
        self.edit_sequence_button.hide()

    def update_preview(self, index):
        if index == None:
            self.image_label.setText("Select a sequence to preview it here!")
            self._adjust_label_for_text()

            self.variation_number_label.setText("")
            return
        if self.thumbnails and index is not None:
            pixmap = QPixmap(self.thumbnails[index])
            self._scale_pixmap_to_label(pixmap)

        if self.current_thumbnail_box:
            self.sequence_json = self.current_thumbnail_box.main_widget.metadata_extractor.extract_metadata_from_file(
                self.thumbnails[index]
            )

    def _scale_pixmap_to_label(self, pixmap: QPixmap):
        label_width = self.image_label.width()
        aspect_ratio = pixmap.height() / pixmap.width()
        new_height = int(label_width * aspect_ratio)
        # if the new height exceeds the height of the preview widget, then we need to make sure that it is scaled down
        if new_height > self.height() * 0.8:
            new_height = int(self.height() * 0.8)
            label_width = int(new_height / aspect_ratio)

        scaled_pixmap = pixmap.scaled(
            label_width,
            new_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setMinimumHeight(new_height)

    def _adjust_label_for_text(self):
        min_height = int(max(self.height() / 5, 50))
        self.image_label.setMinimumHeight(min_height)

    def select_thumbnail(self, thumbnail_box, index, base_word):
        self.current_index = index
        self.base_word = base_word
        self.current_thumbnail_box = thumbnail_box
        self.update_base_word_label()
        self.update_variation_number_label()
        self.update_thumbnails(self.thumbnails)
        self.update_nav_buttons()
        self.update_preview(index)

    def update_nav_buttons(self):
        self.nav_buttons_widget.current_index = self.current_index
        self.nav_buttons_widget.refresh()

    def update_variation_number_label(self):
        if len(self.thumbnails) > 1:
            self.variation_number_label.setText(f"Variation {self.current_index + 1}")
        else:
            self.variation_number_label.setText("")

    def update_base_word_label(self):
        self.base_word_label.setText(self.base_word)

    def edit_sequence(self):
        if not hasattr(self, "sequence_populator"):
            self.sequence_populator = self.dictionary_widget.sequence_populator
        if self.sequence_json:
            self.main_widget.setCurrentIndex(self.main_widget.builder_tab_index)
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            self.sequence_populator.load_sequence_from_json(self.sequence_json)
            QApplication.restoreOverrideCursor()
        else:
            QMessageBox.warning(
                self, "No Selection", "Please select a thumbnail first."
            )

    def showEvent(self, event):
        super().showEvent(event)
        if self.thumbnails and self.current_index is not None:
            self.update_preview(self.current_index)
        else:
            self._adjust_label_for_text()

    def reset_preview_area(self):
        self.current_index = None
        self.update_preview(None)
        self.variation_number_label.setText("")
        self.base_word = ""
        self.base_word_label.setText(self.base_word)
