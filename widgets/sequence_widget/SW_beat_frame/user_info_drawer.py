from typing import TYPE_CHECKING, Dict
from PyQt6.QtGui import QPainter, QFont, QFontMetrics, QImage
from PyQt6.QtCore import Qt
from datetime import datetime

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.image_creator import ImageCreator
    from widgets.sequence_widget.SW_beat_frame.image_drawer import ImageDrawer


class UserInfoDrawer:
    def __init__(self, image_creator: "ImageCreator"):
        self.image_creator = image_creator
        self.font_bold_italic = QFont("Georgia", 50, QFont.Weight.Bold)
        self.font_italic = QFont("Georgia", 50, QFont.Weight.Normal)

    def draw_user_info(
        self,
        image: QImage,
        options: Dict[str, any],
        num_filled_beats: int,
    ) -> None:

        margin = 50
        if num_filled_beats == 1:
            margin = 15
        elif num_filled_beats == 2:
            margin = 25

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        user_name = options.get("user_name", "TacoCat")
        export_date = self._format_export_date(
            options.get("export_date", datetime.now().strftime("%m-%d-%Y"))
        )
        add_info = options.get("add_info", False)
        notes = options.get("notes", "No notes!")

        font_bold_italic = self.font_bold_italic
        font_italic = self.font_italic
        if num_filled_beats == 1:
            font_bold_italic = self._create_font(
                font_bold_italic.family(),
                font_bold_italic.pointSize() // 2,
                font_bold_italic.weight(),
                font_bold_italic.italic(),
            )
            font_italic = self._create_font(
                font_italic.family(),
                font_italic.pointSize() // 2,
                font_italic.weight(),
                font_italic.italic(),
            )
        elif num_filled_beats == 2:
            font_bold_italic = self._create_font(
                font_bold_italic.family(),
                int(font_bold_italic.pointSize() // 1.5),
                font_bold_italic.weight(),
                font_bold_italic.italic(),
            )
            font_italic = self._create_font(
                font_italic.family(),
                int(font_italic.pointSize() // 1.5),
                font_italic.weight(),
                font_italic.italic(),
            )
        # Calculate text widths
        export_date_width = self._get_text_width(font_italic, export_date)
        notes_width = self._get_text_width(font_italic, notes)

        if add_info:
            # Draw user name
            self._draw_text(
                painter, image, user_name, font_bold_italic, margin, "bottom-left"
            )

            # Draw notes text
            self._draw_text(
                painter,
                image,
                notes,
                font_italic,
                margin,
                "bottom-center",
                notes_width,
            )

            # Draw export date
            self._draw_text(
                painter,
                image,
                export_date,
                font_italic,
                margin,
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

        if position == "bottom-left":
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
