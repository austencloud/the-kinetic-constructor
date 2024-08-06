from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter, QFont, QFontMetrics, QImage

from widgets.sequence_widget.SW_beat_frame.font_margin_helper import FontMarginHelper

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.image_creator import ImageCreator


class WordDrawer:
    def __init__(self, image_creator: "ImageCreator"):
        self.image_creator = image_creator
        self.base_font = QFont("Georgia", 175, QFont.Weight.DemiBold, False)
        self.kerning = int(20 * image_creator.beat_scale)  # Adjust this value as needed

    def draw_word(self, image: QImage, word: str, num_filled_beats: int) -> None:
        base_margin = 50 * self.image_creator.beat_scale
        font, margin = FontMarginHelper.adjust_font_and_margin(
            self.base_font, num_filled_beats, base_margin, self.image_creator.beat_scale
        )

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        metrics = QFontMetrics(font)
        text_width = metrics.horizontalAdvance(word)

        # Adjust the font size until the text fits within the image width
        while text_width + 2 * margin > image.width():
            font_size = font.pointSize() - 1
            if font_size <= 10:
                break
            font = QFont(font.family(), font_size, font.weight(), font.italic())
            metrics = QFontMetrics(font)
            text_width = metrics.horizontalAdvance(word)

        self._draw_text(painter, image, word, font, margin, "top")
        painter.end()

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
        metrics = QFontMetrics(font)
        text_height = metrics.ascent()

        if not text_width:
            text_width = metrics.horizontalAdvance(text)

        if position == "top":
            x = (image.width() - text_width - self.kerning * (len(text) - 1)) // 2
            y = int(text_height + margin)

        for letter in text:
            painter.drawText(x, y, letter)
            x += metrics.horizontalAdvance(letter) + self.kerning
