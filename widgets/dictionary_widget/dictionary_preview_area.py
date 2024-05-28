from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QIcon
from preview_area_image_label import PreviewAreaImageLabel
from widgets.dictionary_widget.dictionary_button_panel import DictionaryButtonPanel
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
    edit_sequence_button: QPushButton
    delete_variation_button: QPushButton
    delete_word_button: QPushButton

    def __init__(self, dictionary_widget: "DictionaryWidget"):
        super().__init__(dictionary_widget)
        self.thumbnails = []
        self.current_index = 0
        self.main_widget = dictionary_widget.main_widget
        self.dictionary_widget = dictionary_widget
        self.export_manager = (
            dictionary_widget.main_widget.top_builder_widget.sequence_widget.beat_frame.export_manager
        )
        self.sequence_json = None
        self.current_thumbnail_box: ThumbnailBox = None
        self.base_word = ""
        self._setup_components()

        self.variation_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_panel = DictionaryButtonPanel(self)
        self.update_thumbnails()

        self._setup_layout()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.base_word_label)
        self.layout.addWidget(self.variation_number_label)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.nav_buttons_widget)
        self.layout.addWidget(self.button_panel)
        self.layout.addStretch(1)

    def get_thumbnail_at_current_index(self):
        if self.thumbnails:
            return self.thumbnails[self.current_index]
        return None

    def _setup_button(
        self, button_name: str, icon_path: str, callback, tooltip: str
    ) -> None:
        icon = QIcon(icon_path)
        button = QPushButton(icon, "")
        button.clicked.connect(callback)
        button.setToolTip(tooltip)  # Set the tooltip for the button
        setattr(self, f"{button_name}_button", button)

    def _setup_components(self):
        self.variation_number_label = VariationNumberLabel(self)
        self.base_word_label = BaseWordLabel(self)
        self.image_label = PreviewAreaImageLabel(self)
        self.nav_buttons_widget = PreviewAreaNavButtonsWidget(self)
        self.image_label.setText("Select a sequence to display it here.")

    def update_thumbnails(self, thumbnails=[]):
        self.thumbnails = thumbnails
        self.current_index = 0

        if self.thumbnails:
            self.base_word_label.show()
            self.variation_number_label.show()
            self.button_panel.delete_word_button.show()
            self.button_panel.save_image_button.show()
            self.button_panel.delete_variation_button.show()
            self.button_panel.edit_sequence_button.show()
            self.update_preview(self.current_index)
        else:
            self.base_word_label.hide()
            self.variation_number_label.hide()
            self.button_panel.delete_word_button.hide()
            self.button_panel.save_image_button.hide()
            self.button_panel.delete_variation_button.hide()
            self.button_panel.edit_sequence_button.hide()
            self.image_label.setText("No sequences to display.")
            self._adjust_label_for_text()
            self.update_preview(None)
            return

        if len(self.thumbnails) > 1:
            self.nav_buttons_widget.show()
            self.variation_number_label.show()
        elif len(self.thumbnails) == 1:
            self.nav_buttons_widget.hide()
            self.variation_number_label.hide()

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
            metadata_extractor = (
                self.current_thumbnail_box.main_widget.metadata_extractor
            )
            self.sequence_json = metadata_extractor.extract_metadata_from_file(
                self.thumbnails[index]
            )

    def _scale_pixmap_to_label(self, pixmap: QPixmap):
        label_width = self.image_label.width()
        aspect_ratio = pixmap.height() / pixmap.width()
        new_height = int(label_width * aspect_ratio)
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

    def showEvent(self, event):
        super().showEvent(event)
        if self.thumbnails and self.current_index is not None:
            self.update_preview(self.current_index)
        else:
            self._adjust_label_for_text()
        font_size = self.width() // 20
        placeholder_text_font_size = self.width() // 40
        self.base_word_label.setFont(QFont("Georgia", font_size, QFont.Weight.DemiBold))
        self.image_label.setStyleSheet(
            f"font: {placeholder_text_font_size}pt Arial; font-weight: bold;"
        )
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def reset_preview_area(self):
        self.current_index = None
        self.update_preview(None)
        self.variation_number_label.setText("")
        self.base_word = ""
        self.base_word_label.setText(self.base_word)
