from typing import TYPE_CHECKING, Dict, Tuple, Callable
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QApplication,
    QMessageBox,
)
from PyQt6.QtCore import QSize, Qt, QEvent
from PyQt6.QtGui import QColor, QPixmap

from .sequence_viewer_action_button import SequenceViewerActionButton
from utilities.path_helpers import get_images_and_data_path
from ...full_screen_image_overlay import FullScreenImageOverlay
from ..temp_beat_frame.temp_beat_frame import TempBeatFrame

if TYPE_CHECKING:
    from .sequence_viewer import SequenceViewer


class SequenceViewerActionButtonPanel(QWidget):
    BUTTON_CONFIGS: Dict[str, Tuple[str, str, str]] = {
        "edit_sequence": ("edit.svg", "Edit Sequence", "edit_sequence"),
        "save_image": ("save_image.svg", "Save Image", "save_image"),
        "delete_variation": ("delete.svg", "Delete Variation", "delete_variation"),
        "view_full_screen": ("eye.png", "View Full Screen", "view_full_screen"),
    }

    BUTTON_SIZE_FACTOR = 10
    ICON_SIZE_FACTOR = 0.8

    NO_SEQUENCE_TITLE = "No Selection"
    NO_SEQUENCE_MSG = "Please select a sequence first."

    def __init__(self, sequence_viewer: "SequenceViewer") -> None:
        super().__init__(sequence_viewer)
        self.sequence_viewer: SequenceViewer = sequence_viewer
        self.browse_tab = sequence_viewer.browse_tab
        self.temp_beat_frame = TempBeatFrame(self.browse_tab)

        self.buttons: Dict[str, SequenceViewerActionButton] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        self._setup_buttons()
        self._create_layout()

    def _setup_buttons(self) -> None:
        self.buttons.clear()
        btn_size = int(self.browse_tab.width() // self.BUTTON_SIZE_FACTOR)

        for key, (icon_filename, tooltip, action_name) in self.BUTTON_CONFIGS.items():
            icon_path = get_images_and_data_path(
                f"images/icons/sequence_workbench_icons/{icon_filename}"
            )
            action_method = getattr(self, action_name)
            button = self._create_button(icon_path, tooltip, action_method, btn_size)
            self.buttons[key] = button

    def _create_button(
        self,
        icon_path: str,
        tooltip: str,
        on_click: Callable,
        btn_size: int,
    ) -> SequenceViewerActionButton:
        button = SequenceViewerActionButton(icon_path, tooltip, self)
        button.clicked.connect(on_click)

        icon_size = int(btn_size * self.ICON_SIZE_FACTOR)
        button.setFixedSize(QSize(btn_size, btn_size))
        button.setIconSize(QSize(icon_size, icon_size))
        button.setColor(QColor("white"))
        button.default_color = QColor("white")
        return button

    def _create_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(10)

        self.layout.addStretch(2)

        for button in self.buttons.values():
            self.layout.addWidget(button)
            self.layout.addStretch(1)

        self.layout.addStretch(1)

    def _show_message(self, title: str, message: str) -> None:
        QMessageBox.warning(self, title, message)

    def _get_current_thumbnail(self) -> QPixmap | None:
        return self.sequence_viewer.get_thumbnail_at_current_index()

    def _get_current_thumbnail_or_warn(self) -> QPixmap | None:
        pixmap = self._get_current_thumbnail()
        if not pixmap:
            self._show_message(self.NO_SEQUENCE_TITLE, self.NO_SEQUENCE_MSG)
            return None
        return pixmap

    def _get_sequence_json_or_warn(self) -> dict | None:
        sequence_json = self.sequence_viewer.sequence_json
        if not sequence_json:
            self._show_message(self.NO_SEQUENCE_TITLE, self.NO_SEQUENCE_MSG)
            return None
        return sequence_json

    def view_full_screen(self) -> None:
        seq = self._get_sequence_json_or_warn()
        if not seq:
            return

        pixmap = self._get_current_thumbnail_or_warn()
        if not pixmap:
            return

        overlay = FullScreenImageOverlay(self.sequence_viewer.main_widget)
        overlay.show(QPixmap(pixmap))
        self.sequence_viewer.main_widget.full_screen_overlay = overlay

    def edit_sequence(self) -> None:
        sequence_json = self._get_sequence_json_or_warn()
        if not sequence_json:
            return

        self.sequence_viewer.main_widget.menu_bar.navigation_widget.on_button_clicked(
            self.sequence_viewer.main_widget.main_construct_tab_index
        )

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            self.browse_tab.main_widget.sequence_workbench.beat_frame.populator.populate_beat_frame_from_json(
                sequence_json["sequence"]
            )
        except KeyError:
            self._show_message("Error", "No sequence data found.")
        finally:
            QApplication.restoreOverrideCursor()

    def delete_variation(self) -> None:
        seq = self._get_sequence_json_or_warn()
        if not seq:
            return

        if not self.sequence_viewer.thumbnails:
            self._show_message(self.NO_SEQUENCE_TITLE, self.NO_SEQUENCE_MSG)
            return

        if not self.sequence_viewer.current_thumbnail_box:
            return

        self.browse_tab.deletion_handler.delete_variation(
            self.sequence_viewer.current_thumbnail_box,
            self.sequence_viewer.current_thumbnail_box.current_index,
        )

    def save_image(self) -> None:
        sequence_json = self._get_sequence_json_or_warn()
        if not sequence_json or not self.sequence_viewer.thumbnails:
            return

        pixmap = self._get_current_thumbnail_or_warn()
        if not pixmap:
            return

        self.temp_beat_frame.populate_beat_frame_from_json(sequence_json["sequence"])

        self.temp_beat_frame.export_manager.dialog_executor.exec_dialog(
            sequence_json["sequence"]
        )

    def resizeEvent(self, event: QEvent) -> None:
        self._style_all_buttons()
        super().resizeEvent(event)

    def _style_all_buttons(self) -> None:
        btn_size = int(self.sequence_viewer.main_widget.width() // 30)
        for button in self.buttons.values():
            icon_size = int(btn_size * self.ICON_SIZE_FACTOR)
            button.setFixedSize(QSize(btn_size, btn_size))
            button.setIconSize(QSize(icon_size, icon_size))
            button.setColor(QColor("white"))
            button.default_color = QColor("white")
