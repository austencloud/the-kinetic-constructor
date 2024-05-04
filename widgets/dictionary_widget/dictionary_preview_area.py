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
from PyQt6.QtGui import QPixmap

from path_helpers import get_images_and_data_path
from widgets.dictionary_widget.thumbnail_box.base_word_label import BaseWordLabel
from widgets.dictionary_widget.thumbnail_box.preview_area_nav_btns import (
    PreviewAreaNavButtonsWidget,
)
from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox

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
        self.sequence_populator = dictionary_widget.sequence_populator
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
        self.layout.addWidget(self.nav_buttons)
        self.layout.addWidget(self.edit_sequence_button)
        self.layout.addWidget(self.delete_variation_button)
        self.layout.addWidget(self.delete_word_button)
        self.layout.addStretch(1)

    def _setup_components(self):
        self.variation_number_label = VariationNumberLabel(self.current_index)
        self.base_word_label = BaseWordLabel(self.base_word)
        self.image_label = QLabel("Select a sequence to preview it here!", self)
        self.nav_buttons = PreviewAreaNavButtonsWidget(self)
        self.edit_sequence_button = QPushButton("Edit Sequence")
        self.edit_sequence_button.clicked.connect(self.edit_sequence)
        self.delete_variation_button = QPushButton("Delete Variation", self)
        self.delete_variation_button.clicked.connect(self.confirm_delete_variation)
        self.delete_word_button = QPushButton("Delete Base Word", self)
        self.delete_word_button.clicked.connect(self.confirm_delete_word)

    def confirm_delete_variation(self):
        if not self.current_thumbnail_box:
            QMessageBox.warning(
                self, "No Selection", "Please select a variation first."
            )
            return
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete this variation of {self.base_word}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.dictionary_widget.deletion_manager.delete_variation(
                self.current_thumbnail_box, self.current_index
            )

    def confirm_delete_word(self):
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete all variations of {self.base_word}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.dictionary_widget.deletion_manager.delete_word(self.base_word)




    def update_after_deletion(self):
        # Refresh the UI and internal state after deletion
        self.thumbnails.pop(self.current_index) if self.thumbnails else None
        self.current_index = max(0, self.current_index - 1)
        self.dictionary_widget.browser.scroll_widget.load_base_words()  # Assuming this method reloads the display
        self.update_preview(self.current_index if self.thumbnails else None)

    def update_thumbnails(self, thumbnails=[]):
        self.thumbnails = thumbnails
        if self.thumbnails:
            self.nav_buttons.enable_buttons(True)
        else:
            self.nav_buttons.enable_buttons(False)
            self.update_preview(None)

    def update_preview(self, index):
        # if the index is none, display the default text
        if index == None:
            self.image_label.setText("Select a sequence to preview it here!")
            self._adjust_label_for_text()
            # set the base word label to ""
            # self.base_word_label.setText("")
            self.variation_number_label.setText("")
            return
        if self.thumbnails and index is not None:
            pixmap = QPixmap(self.thumbnails[index])
            self._scale_pixmap_to_label(pixmap)

        # extract the json and save it as self.sequence_json
        if self.current_thumbnail_box:
            self.sequence_json = self.current_thumbnail_box.metadata_extractor.extract_metadata_from_file(
                self.thumbnails[index]
            )

    def _scale_pixmap_to_label(self, pixmap: QPixmap):
        label_width = self.image_label.width()
        aspect_ratio = pixmap.height() / pixmap.width()
        new_height = int(label_width * aspect_ratio)
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
        self.update_thumbnails(self.thumbnails)
        self.update_preview(index)

    def update_base_word_label(self):
        self.base_word_label.setText(self.base_word)

    def _setup_preview_image_label(self):
        default_text = "Select a sequence to display it here."
        self.image_label = QLabel(default_text)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def edit_sequence(self):
        if self.sequence_json:
            self.main_widget.setCurrentIndex(self.main_widget.builder_tab_index)
            self.sequence_populator.load_sequence_from_json(self.sequence_json)

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
