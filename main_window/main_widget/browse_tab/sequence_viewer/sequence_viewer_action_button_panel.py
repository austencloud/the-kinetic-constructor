from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QApplication, QMessageBox
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap, QResizeEvent
from ...full_screen_image_overlay import FullScreenImageOverlay
from ..temp_beat_frame.temp_beat_frame import TempBeatFrame
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from .sequence_viewer import SequenceViewer


class SequenceViewerActionButtonPanel(QWidget):
    delete_variation_button: QPushButton
    edit_sequence_button: QPushButton
    save_image_button: QPushButton

    def __init__(self, sequence_viewer: "SequenceViewer"):
        super().__init__(sequence_viewer)
        self.sequence_viewer = sequence_viewer
        self.browse_tab = sequence_viewer.browse_tab
        self.temp_beat_frame = TempBeatFrame(self.browse_tab)
        self._setup_buttons()

    def _setup_buttons(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(10)

        buttons_data = {
            "edit_sequence": {
                "icon": "edit.svg",
                "tooltip": "Edit Sequence",
                "action": self.edit_sequence,
            },
            "save_image": {
                "icon": "save_image.svg",
                "tooltip": "Save Image",
                "action": self.save_image,
            },
            "delete_variation": {
                "icon": "delete.svg",
                "tooltip": "Delete Variation",
                "action": lambda: (
                    self.browse_tab.deletion_handler.delete_variation(
                        self.sequence_viewer.current_thumbnail_box,
                        ((self.sequence_viewer.current_thumbnail_box.current_index)),
                    )
                    if self.sequence_viewer.current_thumbnail_box
                    else None
                ),
            },
            "view_full_screen": {
                "icon": "eye.png",  # Eye icon for full screen
                "tooltip": "View Full Screen",
                "action": self.view_full_screen,
            },
        }

        self.layout.addStretch(2)
        for key, data in buttons_data.items():
            icon_path = get_images_and_data_path(
                f"images/icons/sequence_widget_icons/{data['icon']}"
            )
            button = QPushButton(QIcon(icon_path), "", self, toolTip=data["tooltip"])
            button.setToolTip(data["tooltip"])
            if data["action"]:
                button.clicked.connect(data["action"])
            self.layout.addWidget(button)
            self.layout.addStretch(1)
            setattr(self, f"{key}_button", button)
            btn_size = int(self.browse_tab.width() // 10)
            icon_size = int(btn_size * 0.8)
            button.setMinimumSize(QSize(btn_size, btn_size))
            button.setMaximumSize(QSize(btn_size, btn_size))
            button.setIconSize(QSize(icon_size, icon_size))
            button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.layout.addStretch(1)

    def view_full_screen(self):
        """Display the current image in full screen mode."""
        current_thumbnail = self.sequence_viewer.get_thumbnail_at_current_index()
        mw = self.sequence_viewer.main_widget
        if current_thumbnail:
            pixmap = QPixmap(current_thumbnail)
            mw.full_screen_overlay = FullScreenImageOverlay(mw)
            mw.full_screen_overlay.show(pixmap)
        else:
            QMessageBox.warning(self, "No Image", "Please select an image first.")

    def edit_sequence(self):
        if not hasattr(self, "sequence_populator"):
            self.sequence_populator = self.browse_tab.edit_sequence_handler
        if self.sequence_viewer.sequence_json:
            self.sequence_viewer.main_widget.navigation_widget.on_button_clicked(0)
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            self.sequence_populator.load_sequence_from_json(
                self.sequence_viewer.sequence_json
            )
            QApplication.restoreOverrideCursor()
        else:
            QMessageBox.warning(
                self, "No Selection", "Please select a thumbnail first."
            )

    def save_image(self):
        current_thumbnail = self.sequence_viewer.get_thumbnail_at_current_index()
        if not current_thumbnail:
            QMessageBox.warning(
                self, "No Selection", "Please select a thumbnail first."
            )
            return

        metadata = self.sequence_viewer.sequence_json
        if not metadata:
            QMessageBox.warning(
                self, "No Metadata", "No metadata found for the selected sequence."
            )
            return

        self.temp_beat_frame.populate_beat_frame_from_json(metadata["sequence"])
        self.export_manager = self.temp_beat_frame.export_manager
        self.export_manager.dialog_executor.exec_dialog(metadata["sequence"])

    def hide_buttons(self):
        self.save_image_button.hide()
        self.delete_variation_button.hide()
        self.edit_sequence_button.hide()

    def show_buttons(self):
        self.save_image_button.show()
        self.delete_variation_button.show()
        self.edit_sequence_button.show()

    def resizeEvent(self, event: QResizeEvent) -> None:
        btn_size = int(self.sequence_viewer.main_widget.width() // 30)
        icon_size = int(btn_size * 0.8)
        for button_name in [
            "edit_sequence",
            "save_image",
            "delete_variation",
            "view_full_screen",
        ]:
            button: QPushButton = getattr(self, f"{button_name}_button")
            button.setMinimumSize(QSize(btn_size, btn_size))
            button.setMaximumSize(QSize(btn_size, btn_size))
            button.setIconSize(QSize(icon_size, icon_size))
        super().resizeEvent(event)
