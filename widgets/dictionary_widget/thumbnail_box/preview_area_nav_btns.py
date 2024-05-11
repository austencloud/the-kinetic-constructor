from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_preview_area import DictionaryPreviewArea
    from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox


class PreviewAreaNavButtonsWidget(QWidget):
    def __init__(self, preview_area: "DictionaryPreviewArea"):
        super().__init__(preview_area)
        self.preview_area = preview_area
        self.thumbnails = preview_area.thumbnails
        self.current_index = preview_area.current_index
        self.variation_number_label = preview_area.variation_number_label
        self.image_label = preview_area.image_label
        self._setup_buttons()
        self.has_multiple_thumbnails = len(self.thumbnails) > 1
        if not self.has_multiple_thumbnails:
            self.hide()

    def _setup_buttons(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.buttons = []
        self.left_button = PreviewAreaNavButton("<", self)
        self.right_button = PreviewAreaNavButton(">", self)
        self.layout.addWidget(self.left_button)
        self.layout.addWidget(self.right_button)

    def handle_button_click(self):
        if not self.preview_area.thumbnails:
            return
        sender = self.sender()
        if sender.text() == "<":
            self.preview_area.current_index = (
                self.preview_area.current_index - 1
            ) % len(self.preview_area.thumbnails)
        elif sender.text() == ">":
            self.preview_area.current_index = (
                self.preview_area.current_index + 1
            ) % len(self.preview_area.thumbnails)
        QApplication.processEvents()
        self.preview_area.update_preview(self.preview_area.current_index)
        QApplication.processEvents()
        self.preview_area.variation_number_label.setText(
            f"Variation {self.preview_area.current_index+ 1}"
        )

        self.preview_area.current_thumbnail_box.current_index = (
            self.preview_area.current_index
        )
        box_nav_buttons_widget = (
            self.preview_area.current_thumbnail_box.nav_buttons_widget
        )
        box_nav_buttons_widget.current_index = self.preview_area.current_index
        box_nav_buttons_widget.update_thumbnail()

    def update_thumbnail(self):
        self.image_label.current_index = self.current_index
        self.image_label.update_thumbnail()
        self.variation_number_label.update_index(self.current_index)

    def refresh(self):
        thumbnails = self.preview_area.thumbnails
        are_multiple_thumbnails = len(thumbnails) > 1
        self.left_button.setEnabled(are_multiple_thumbnails)
        self.right_button.setEnabled(are_multiple_thumbnails)
        self.update_thumbnail()
        if len(thumbnails) == 1:
            self.variation_number_label.hide()
            self.hide()
        else:
            self.variation_number_label.show()
            self.show()
            self.variation_number_label.update_index(self.current_index + 1)


class PreviewAreaNavButton(QPushButton):
    def __init__(self, text: str, parent: PreviewAreaNavButtonsWidget):
        super().__init__(text, parent)
        self.clicked.connect(parent.handle_button_click)
        self.setStyleSheet("background-color: white;")
        self.setFont(QFont("Arial", 16, QFont.Weight.Bold))

    def enterEvent(self, event):
        self.setStyleSheet("background-color: lightgray;")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def leaveEvent(self, event):
        self.setStyleSheet("background-color: white;")
        self.setCursor(Qt.CursorShape.ArrowCursor)
