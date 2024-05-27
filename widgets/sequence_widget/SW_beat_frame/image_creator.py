from PyQt6.QtGui import QImage
from PyQt6.QtCore import Qt
import os
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QImage

from path_helpers import get_my_photos_path
from widgets.sequence_widget.SW_beat_frame.beat import Beat, BeatView

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.sequence_image_export_manager import (
        SequenceImageExportManager,
    )


class ImageCreator:
    def __init__(self, export_manager: "SequenceImageExportManager"):
        self.export_manager = export_manager
        self.beat_frame = export_manager.beat_frame
        self.indicator_label = export_manager.indicator_label
        self.sequence_widget = export_manager.sequence_widget
        self.layout_manager = export_manager.layout_manager
        self.image_drawer = export_manager.image_drawer
        self.beat_size = self.beat_frame.start_pos_view.beat.width()
        self.beat_factory = export_manager.beat_factory


class ImageCreator:
    def __init__(self, export_manager: "SequenceImageExportManager"):
        self.export_manager = export_manager
        self.beat_frame = export_manager.beat_frame
        self.layout_manager = export_manager.layout_manager
        self.image_drawer = export_manager.image_drawer
        self.beat_size = self.beat_frame.start_pos_view.beat.width()
        self.beat_factory = export_manager.beat_factory

    def create_sequence_image(
        self, sequence: list[dict], include_start_pos=True, options: dict = None
    ) -> QImage:
        filled_beats = self.beat_factory.process_sequence_to_beats(sequence)
        column_count, row_count = self.layout_manager.calculate_layout(
            len(filled_beats), include_start_pos
        )

        additional_height_top = 300 if options.get("add_word", False) else 0
        additional_height_bottom = 150 if options.get("add_info", False) else 0

        image = self._create_image(
            column_count, row_count, additional_height_top + additional_height_bottom
        )
        self.image_drawer.draw_beats(
            image,
            filled_beats,
            column_count,
            row_count,
            include_start_pos,
            additional_height_top,
        )
        if options.get("add_info", False):
            self.image_drawer.draw_user_info(image, options)
        return image

    def _create_image(self, column_count, row_count, additional_height=0) -> QImage:
        image_width = int(column_count * self.beat_size)
        image_height = int(row_count * self.beat_size + additional_height)
        image = QImage(image_width, image_height, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)
        return image
