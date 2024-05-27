from typing import TYPE_CHECKING, List, Dict
from PyQt6.QtGui import QPainter, QFont, QPixmap, QImage, QFontMetrics
from PyQt6.QtCore import Qt
from datetime import datetime

from widgets.sequence_widget.SW_beat_frame.beat import BeatView

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.sequence_image_export_manager import (
        SequenceImageExportManager,
    )


class ImageDrawer:
    def __init__(self, export_manager: "SequenceImageExportManager"):
        self.export_manager = export_manager
        self.beat_frame = export_manager.beat_frame
        self.margin = 50

        # Fonts
        self.font_bold_italic = self._create_font(
            "Georgia", 50, QFont.Weight.Bold, True
        )
        self.font_italic = self._create_font("Georgia", 50, QFont.Weight.Normal, True)
        self.font_word = self._create_font("Georgia", 175, QFont.Weight.DemiBold, False)

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

    def draw_user_info(self, image: QImage, options: Dict[str, any]) -> None:
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        user_name = options.get("user_name", "TacoCat")
        export_date = self._format_export_date(
            options.get("export_date", datetime.now().strftime("%m-%d-%Y"))
        )
        add_word = options.get("add_word", False)
        word = self.beat_frame.get_current_word() if add_word else ""
        notes = options.get("notes", "No notes! ")

        # Calculate text widths
        export_date_width = self._get_text_width(self.font_italic, export_date)
        notes_width = self._get_text_width(self.font_italic, notes)

        # draw word
        if add_word:
            self._draw_text(painter, image, word, self.font_word, self.margin, "top")

        # draw user name
        self._draw_text(
            painter, image, user_name, self.font_bold_italic, self.margin, "bottom-left"
        )

        # draw notes text
        self._draw_text(
            painter,
            image,
            notes,
            self.font_italic,
            self.margin,
            "bottom-center",
            notes_width,
        )
        # draw export date
        self._draw_text(
            painter,
            image,
            export_date,
            self.font_italic,
            self.margin,
            "bottom-right",
            export_date_width,
        )

        painter.end()

    def _create_font(self, family: str, size: int, weight: int, italic: bool) -> QFont:
        font = QFont(family, size, weight)
        font.setItalic(italic)
        return font

    def _format_export_date(self, date_str: str) -> str:
        return "-".join([str(int(part)) for part in date_str.split("-")])

    def _draw_text(
        self,
        painter: QPainter,
        image: QImage,
        text: str,
        font: QFont,
        margin: int,
        position: str,
        text_width: int = None,
    ) -> None:
        painter.setFont(font)
        if not text_width:
            metrics = QFontMetrics(font)
            text_width = metrics.horizontalAdvance(text)
            text_height = metrics.ascent()
        else:
            metrics = QFontMetrics(font)
            text_height = metrics.ascent()

        if position == "top":
            x = (image.width() - text_width) // 2
            y = text_height
        elif position == "bottom-left":
            x = margin
            y = image.height() - margin
        elif position == "bottom-center":
            x = (image.width() - text_width) // 2
            y = image.height() - margin
        elif position == "bottom-right":
            x = image.width() - text_width - margin
            y = image.height() - margin

        painter.drawText(x, y, text)

    def _get_text_width(self, font: QFont, text: str) -> int:
        metrics = QFontMetrics(font)
        return metrics.horizontalAdvance(text)

    def _grab_pixmap(self, view: "BeatView", width: int, height: int) -> QPixmap:
        return view.grab().scaled(
            width,
            height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
