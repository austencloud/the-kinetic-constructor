from typing import TYPE_CHECKING, List
from PyQt6.QtGui import QPainter, QImage, QPixmap
from PyQt6.QtCore import Qt
from widgets.sequence_widget.SW_beat_frame.beat import BeatView
if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.image_creator import ImageCreator


class BeatDrawer:
    def __init__(self, image_creator: "ImageCreator"):
        self.image_creator = image_creator
        self.beat_frame = image_creator.export_manager.beat_frame

    def draw_beats(
        self,
        image: QImage,
        filled_beats: List[BeatView],
        column_count: int,
        row_count: int,
        include_start_pos: bool,
        additional_height_top: int,
    ) -> None:
        beat_size = int(self.beat_frame.start_pos_view.beat.width())
        painter = QPainter(image)
        beat_number = 0

        if include_start_pos:
            start_pos_pixmap = self._grab_pixmap(
                self.beat_frame.start_pos_view, beat_size, beat_size
            )
            painter.drawPixmap(0, additional_height_top, start_pos_pixmap)
            start_col = 1
        else:
            start_col = 0

        for row in range(row_count + 1):
            for col in range(start_col, column_count):
                if beat_number < len(filled_beats):
                    beat_view = filled_beats[beat_number]
                    beat_pixmap = self._grab_pixmap(beat_view, beat_size, beat_size)
                    target_x = col * beat_size
                    target_y = row * beat_size + additional_height_top
                    painter.drawPixmap(target_x, target_y, beat_pixmap)
                    beat_number += 1

        painter.end()

    def _grab_pixmap(self, view: "BeatView", width: int, height: int) -> QPixmap:
        return view.grab().scaled(
            width,
            height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
