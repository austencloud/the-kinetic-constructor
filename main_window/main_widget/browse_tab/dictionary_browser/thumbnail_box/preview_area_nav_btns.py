from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt



if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.dictionary_preview_area import DictionaryPreviewArea


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
        self.buttons: list[PreviewAreaNavButton] = []
        self.left_button = PreviewAreaNavButton("<", self)
        self.right_button = PreviewAreaNavButton(">", self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.left_button, 6)
        self.layout.addWidget(self.right_button, 6)
        self.layout.addStretch(1)
        
    def handle_button_click(self):
        if not self.preview_area.thumbnails:
            return
        sender: QPushButton = self.sender()
        if sender.text() == "<":
            self.preview_area.current_index = (
                self.preview_area.current_index - 1
            ) % len(self.preview_area.thumbnails)
        elif sender.text() == ">":
            self.preview_area.current_index = (
                self.preview_area.current_index + 1
            ) % len(self.preview_area.thumbnails)
        self.preview_area.update_preview(self.preview_area.current_index)
        self.preview_area.variation_number_label.setText(
            f"{self.preview_area.current_index + 1}/{len(self.preview_area.thumbnails)}"
        )

        self.preview_area.current_thumbnail_box.current_index = (
            self.preview_area.current_index
        )
        box_nav_buttons_widget = (
            self.preview_area.current_thumbnail_box.nav_buttons_widget
        )
        box_nav_buttons_widget.thumbnail_box.current_index = self.preview_area.current_index
        box_nav_buttons_widget.update_thumbnail(self.preview_area.current_index)

    def update_thumbnail(self):
        self.image_label.current_index = self.current_index
        self.image_label.update_thumbnail()
        self.variation_number_label.update_index(self.current_index)

    def refresh(self):
        thumbnails = self.preview_area.thumbnails

        self.update_thumbnail()
        if len(thumbnails) == 1:
            self.variation_number_label.hide()
            self.hide()
        else:
            self.variation_number_label.show()
            self.show()
            self.resize_nav_buttons()
            self.variation_number_label.update_index(self.current_index + 1)

    def resize_nav_buttons(self):
        font_size = self.preview_area.main_widget.width() // 20
        for button in self.buttons:
            button.setFont(QFont("Arial", font_size, QFont.Weight.Bold))

class PreviewAreaNavButton(QPushButton):
    def __init__(self, text: str, parent: PreviewAreaNavButtonsWidget):
        super().__init__(text, parent)
        self.clicked.connect(parent.handle_button_click)
        self.setStyleSheet("background-color: white;")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    