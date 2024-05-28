from datetime import datetime
import os
import subprocess
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPainter, QPixmap, QFont
from path_helpers import get_my_photos_path
from widgets.image_export_dialog.image_export_dialog import ImageExportDialog
from widgets.image_export_layout_handler import ImageExportLayoutHandler
from widgets.sequence_widget.SW_beat_frame.beat import Beat, BeatView
from PyQt6.QtWidgets import QFileDialog

from widgets.sequence_widget.SW_beat_frame.image_creator import ImageCreator
from widgets.sequence_widget.SW_beat_frame.image_drawer import ImageDrawer
from widgets.sequence_widget.SW_beat_frame.image_export_beat_factory import (
    ImageExportBeatFactory,
)
from widgets.sequence_widget.SW_beat_frame.image_export_dialog_executor import (
    ImageExportDialogExecutor,
)
from widgets.sequence_widget.SW_beat_frame.image_saver import ImageSaver

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import SW_BeatFrame


class SequenceImageExportManager:
    last_save_directory = None

    def __init__(self, beat_frame: "SW_BeatFrame") -> None:
        self.beat_frame = beat_frame
        self.main_widget = beat_frame.main_widget
        self.indicator_label = beat_frame.sequence_widget.indicator_label
        self.sequence_widget = beat_frame.sequence_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.include_start_pos = self.settings_manager.get_image_export_setting(
            "include_start_position", True
        )
        self.layout_handler = ImageExportLayoutHandler(self)
        self.image_drawer = ImageDrawer(self)
        self.beat_factory = ImageExportBeatFactory(self)
        self.image_creator = ImageCreator(self)
        self.image_saver = ImageSaver(self)
        self.dialog_executor = ImageExportDialogExecutor(self)

    def exec_dialog(self):
        self.dialog_executor.exec_dialog()
