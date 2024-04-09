from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPainter, QPixmap
from PyQt6.QtWidgets import QFileDialog
from path_helpers import get_my_photos_path

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget_beat_frame.beat import BeatView
    from widgets.sequence_widget.sequence_widget_beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )


class BeatFrameImageExportManager:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame") -> None:
        self.beat_frame = beat_frame
        self.indicator_label = beat_frame.sequence_widget.indicator_label

    def save_image(self) -> None:
        word = self.beat_frame.get_current_word()
        if word == "":
            self.indicator_label.show_message("Nothing to save.")
            return

        # Default save path within the 'My Pictures' folder inside the 'The Kinetic Alphabet' subfolder
        default_save_path = get_my_photos_path(f"{word}.png")

        # Open a file save dialog with the default save path
        # Removed the options initialization and passing; directly use the method
        file_name, _ = QFileDialog.getSaveFileName(
            self.beat_frame,
            "Save Image",
            default_save_path,
            "Images (*.png *.jpeg *.jpg)",
            # You can add options here if needed, for example:
            # options=QFileDialog.Option.DontUseNativeDialog
        )

        if not file_name:
            # User canceled or closed the dialog
            return

        filled_beats = [beat for beat in self.beat_frame.beats if beat.is_filled]
        column_count, row_count = self._calculate_layout(len(filled_beats))
        #deselect everything in each of hte beat scenes
        for beat in filled_beats:
            beat.scene().clearSelection()
        beat_frame_image = self._create_image(column_count, row_count)
        self._draw_beats(beat_frame_image, filled_beats, column_count, row_count)

        beat_frame_image.save(file_name, "PNG")
        # Show a message with the name of the file where it was saved
        self.indicator_label.show_message(f"Image saved as {file_name.split('/')[-1]}")

    def _create_image(self, column_count, row_count) -> QImage:
        self.beat_size = int(self.beat_frame.start_pos_view.beat.width())

        image_width = column_count * self.beat_size
        image_height = row_count * self.beat_size
        image = QImage(image_width, image_height, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)
        return image

    def create_beat_frame_image_for_printing(self) -> QImage:
        word = self.beat_frame.get_current_word()

        filled_beats = [beat for beat in self.beat_frame.beats if beat.is_filled]
        column_count, row_count = self._calculate_layout(len(filled_beats))

        beat_frame_image = self._create_image(column_count, row_count)
        self._draw_beats(beat_frame_image, filled_beats, column_count, row_count)

        return beat_frame_image

    def _draw_beats(self, image, filled_beats, column_count, row_count) -> None:
        painter = QPainter(image)
        beat_number = 0

        # Draw start position
        start_pos_pixmap = self._grab_pixmap(
            self.beat_frame.start_pos_view, self.beat_size, self.beat_size
        )
        painter.drawPixmap(0, 0, start_pos_pixmap)

        # Draw beats
        for row in range(row_count):
            for col in range(1, column_count):  # Start from second column
                if beat_number < len(filled_beats):
                    beat_view = filled_beats[beat_number]
                    beat_pixmap = self._grab_pixmap(
                        beat_view, self.beat_size, self.beat_size
                    )
                    target_x = col * self.beat_size
                    target_y = row * self.beat_size
                    painter.drawPixmap(target_x, target_y, beat_pixmap)
                    beat_number += 1

        painter.end()

    def _grab_pixmap(self, view: "BeatView", width, height) -> QPixmap:
        return view.grab().scaled(
            width,
            height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    def _calculate_layout(self, filled_beat_count) -> tuple[int, int]:
        """Calculate the number of columns and rows based on the number of filled beats."""
        layout_options = self.get_layout_options()

        if filled_beat_count in layout_options:
            return layout_options[filled_beat_count]
        else:
            column_count = min(
                filled_beat_count // self.beat_frame.ROW_COUNT + 1,
                self.beat_frame.COLUMN_COUNT,
            )
            row_count = min(
                (filled_beat_count + column_count - 1) // column_count,
                self.beat_frame.ROW_COUNT,
            )
            return column_count, row_count

    def get_layout_options(self) -> dict[int, tuple[int, int]]:
        layout_options = {
            0: (1, 1),
            1: (2, 1),
            2: (3, 1),
            3: (4, 1),
            4: (3, 2),
            5: (4, 2),
            6: (4, 2),
            8: (5, 2),
            9: (4, 3),
            10: (5, 3),
            11: (5, 3),
            12: (4, 4),
            13: (5, 4),
            14: (5, 4),
            15: (5, 4),
            16: (5, 4),
        }

        return layout_options
