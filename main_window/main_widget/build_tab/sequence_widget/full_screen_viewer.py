from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMessageBox

from main_window.main_widget.browse_tab.full_screen_image_overlay import (
    FullScreenImageOverlay,
)
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.build_tab.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class FullScreenViewer:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget
        self.beat_frame = sequence_widget.beat_frame
        self.indicator_label = sequence_widget.indicator_label
        self.full_screen_overlay = None

    def view_full_screen(self):
        """Display the current image in full screen mode."""
        # Set mouse cursor to waiting
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        last_beat = self.beat_frame.get.last_filled_beat()
        if last_beat.__class__.__name__ == "StartPositionBeatView":
            self.indicator_label.show_message("Please build a sequence first.")
            QApplication.restoreOverrideCursor()
            return
        else:
            current_thumbnail = self.create_thumbnail()
            if current_thumbnail:
                pixmap = QPixmap(current_thumbnail)
                if self.full_screen_overlay:
                    self.full_screen_overlay.close()  # Close any existing overlay
                self.full_screen_overlay = FullScreenImageOverlay(
                    self.main_widget, pixmap
                )
                self.full_screen_overlay.show()
                # Set mouse cursor back to normal
                QApplication.restoreOverrideCursor()
            else:
                QMessageBox.warning(None, "No Image", "Please select an image first.")
                QApplication.restoreOverrideCursor()

    def create_thumbnail(self):
        # Use the image export manager to create a thumbnail
        return self.sequence_widget.add_to_dictionary_manager.thumbnail_generator.generate_and_save_thumbnail(
            self.sequence_widget.json_manager.loader_saver.load_current_sequence_json(),
            0,
            get_images_and_data_path("temp"),
        )
