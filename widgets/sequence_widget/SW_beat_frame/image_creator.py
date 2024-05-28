from PyQt6.QtGui import QImage
from PyQt6.QtCore import Qt
import os
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QImage

from path_helpers import get_my_photos_path
from widgets.sequence_widget.SW_beat_frame.beat import Beat, BeatView
from widgets.sequence_widget.SW_beat_frame.beat_drawer import BeatDrawer
from widgets.sequence_widget.SW_beat_frame.user_info_drawer import UserInfoDrawer
from widgets.sequence_widget.SW_beat_frame.word_drawer import WordDrawer

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.sequence_image_export_manager import (
        SequenceImageExportManager,
    )


class ImageCreator:
    def __init__(self, export_manager: "SequenceImageExportManager"):
        self.export_manager = export_manager
        self.beat_frame = export_manager.beat_frame
        self.layout_manager = export_manager.layout_handler
        self.image_drawer = export_manager.image_drawer
        self.beat_size = self.beat_frame.start_pos_view.beat.width()
        self.beat_factory = export_manager.beat_factory

        self._setup_drawers()

    def _setup_drawers(self):
        self.beat_drawer = BeatDrawer(self)
        self.word_drawer = WordDrawer(self)
        self.user_info_drawer = UserInfoDrawer(self)

    def create_sequence_image(
        self, sequence: list[dict], include_start_pos=True, options: dict = None
    ) -> QImage:
        filled_beats = self.beat_factory.process_sequence_to_beats(sequence)
        column_count, row_count = self.layout_manager.calculate_layout(
            len(filled_beats), include_start_pos
        )
        num_filled_beats = len(filled_beats)
        if num_filled_beats == 1:
            additional_height_top = 200 if options.get("add_word", False) else 0
            additional_height_bottom = 55 if options.get("add_info", False) else 0
        elif num_filled_beats == 2:
            additional_height_top = 200 if options.get("add_word", False) else 0
            additional_height_bottom = 75 if options.get("add_info", False) else 0
        else:
            additional_height_top = 300 if options.get("add_word", False) else 0
            additional_height_bottom = 150 if options.get("add_info", False) else 0

        image = self._create_image(
            column_count, row_count, additional_height_top + additional_height_bottom
        )
        self.beat_drawer.draw_beats(
            image,
            filled_beats,
            column_count,
            row_count,
            include_start_pos,
            additional_height_top,
        )

        if options.get("add_info", False):
            self.user_info_drawer.draw_user_info(
                image, options, num_filled_beats
            )

        if options.get("add_word", False):
            word = self.beat_frame.get_current_word()
            self.word_drawer.draw_word(image, word, num_filled_beats)

        return image

    def _create_image(self, column_count, row_count, additional_height=0) -> QImage:
        image_width = int(column_count * self.beat_size)
        image_height = int(row_count * self.beat_size + additional_height)
        image = QImage(image_width, image_height, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)
        return image
