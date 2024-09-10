from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QRect

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class FullScreenImageOverlay(QWidget):
    def __init__(self, main_widget: "MainWidget", pixmap: QPixmap):
        super().__init__(main_widget)  # Attach to the main widget
        self.main_widget = main_widget

        # Set up the overlay
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
        )  # No borders or title bar

        self.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.9);"
        )  # Semi-transparent black background

        # Layout for the image
        layout = QVBoxLayout(self)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )
        self.image_label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.image_label)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        # Set the image pixmap
        self.set_pixmap_to_fit(pixmap)

        # Set dimensions to match the main widget
        self._set_geometry()

    def _set_geometry(self):
        geometry = QRect()
        geometry.setX(0)
        geometry.setY(0)
        geometry.setHeight(self.main_widget.main_window.height())
        geometry.setWidth(self.main_widget.main_window.width())
        self.setGeometry(geometry)

    def resizeEvent(self, event):
        """Ensure the image is resized correctly when the window is resized."""
        self._set_geometry()
        if self.image_label.pixmap():
            self.set_pixmap_to_fit(self.image_label.pixmap())

    def set_pixmap_to_fit(self, pixmap: QPixmap):
        """Scale the pixmap to fit within the window while maintaining aspect ratio."""
        window_size = self.main_widget.main_window.size()
        # subtrract the height of the tab bar itself from the window size
        tab_bar_height = self.main_widget.get_tab_bar_height()
        menu_bar_height = self.main_widget.main_window.menu_bar_widget.height()
        window_size.setHeight(window_size.height() - tab_bar_height - menu_bar_height)

        scaled_pixmap = pixmap.scaled(
            window_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.image_label.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event):
        """Close the overlay when the image is clicked."""
        self.close()

    def close(self):
        """Close the overlay."""
        super().close()
        self.main_widget.dictionary_widget.preview_area.button_panel.full_screen_overlay = (
            None
        )
