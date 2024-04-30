import math
from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter, QLinearGradient, QColor
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt, QTimer
from widgets.dictionary_widget.dictionary_browser import DictionaryBrowser
from widgets.dictionary_widget.dictionary_sequence_populator import (
    DictionarySequencePopulator,
)
from widgets.dictionary_widget.preview_area import PreviewArea
from widgets.dictionary_widget.thumbnail_box import ThumbnailBox
from .dictionary_variation_manager import DictionaryVariationManager

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class DictionaryWidget(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget
        self.setup_ui()
        self.variation_manager = DictionaryVariationManager(self)
        self.sequence_populator = DictionarySequencePopulator(self)
        self.selected_thumbnail = (
            None  # Initialize the attribute to avoid AttributeError
        )
        self.currently_selected_thumbnail: ThumbnailBox = None

        self.gradient_shift = 0
        self.color_shift = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_background)
        self.timer.start(75)  # Adjust as needed for smoother or faster animation

    def animate_background(self):
        """Update the gradient and color shift for the animation."""
        self.gradient_shift += 0.05  # Adjust for speed of the undulation
        self.color_shift += 1  # Adjust for speed of color change
        if self.color_shift > 360:
            self.color_shift = 0
        self.update()  # Trigger a repaint

    def setup_ui(self):
        h_layout = QHBoxLayout(self)
        self.dictionary_browser = DictionaryBrowser(self)
        h_layout.addWidget(self.dictionary_browser, 3)

        self.preview_area = PreviewArea(self)
        self.preview_area.set_edit_sequence_callback(self.edit_sequence)
        h_layout.addWidget(self.preview_area, 2)

        self.setLayout(h_layout)
        self.dictionary_browser.load_base_words()

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

    def get_metadata_from_thumbnail(self, thumbnail):
        # This is a placeholder, you need to implement logic to extract metadata from the thumbnail
        return {"file_path": "path_to_the_sequence_file.json"}

    def thumbnail_clicked(self, thumbnail_pixmap, metadata):
        # Save the thumbnail metadata when a thumbnail is clicked
        self.selected_thumbnail = metadata
        # Update the preview area with the selected thumbnail pixmap
        self.preview_area.preview_label.setPixmap(
            thumbnail_pixmap.scaled(
                self.preview_area.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.update_selection(self.currently_selected_thumbnail)

    def clear_layout(self, layout: QVBoxLayout):
        """Remove all widgets from a layout."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                elif item.layout() is not None:
                    self.clear_layout(item.layout())

    def update_selection(self, new_selection):
        if self.currently_selected_thumbnail:
            self.currently_selected_thumbnail.set_selected(False)
        self.currently_selected_thumbnail: ThumbnailBox = new_selection
        self.currently_selected_thumbnail.set_selected(True)
        self.thumbnail_clicked(
            self.currently_selected_thumbnail.thumbnail_pixmap,
        )

    def reload_dictionary_tab(self):
        self.dictionary_browser.load_base_words()  # Call load_base_words to refresh the UI

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        for i in range(10):  # Number of bands in the gradient
            pos = i / 10
            hue = int((self.color_shift + pos * 100) % 360)
            color = QColor.fromHsv(hue, 255, 255, 150)  # Adjust the alpha for intensity
            # Calculate undulation effect and clamp values to the 0-1 range
            adjusted_pos = pos + math.sin(self.gradient_shift + pos * math.pi) * 0.05
            clamped_pos = max(0, min(adjusted_pos, 1))  # Clamp between 0 and 1
            gradient.setColorAt(clamped_pos, color)

        painter.fillRect(self.rect(), gradient)
