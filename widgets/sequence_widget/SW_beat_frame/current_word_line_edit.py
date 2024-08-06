from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QApplication,
    QLineEdit,
)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QFont, QFontMetrics, QMouseEvent, QPainter


if TYPE_CHECKING:
    from widgets.sequence_widget.current_word_label import CurrentWordLabel
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class CurrentWordLineEdit(QLineEdit):
    def __init__(self, label: "CurrentWordLabel"):
        super().__init__(label)
        self.label = label
        self.setMouseTracking(True)
        self.setReadOnly(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # Prevent focusing
        self.setStyleSheet(
            """
            QLineEdit {
                background-color: transparent;
                border: none;
                padding-top: 0px;
                padding-bottom: 0px;
                margin: 0px;
                line-height: 1.0em;
                font-family: Georgia;
                font-weight: 600;
            }
            """
        )
        self.setFrame(False)
        self.kerning = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        font = self.font()
        painter.setFont(font)
        metrics = QFontMetrics(font)
        text = self.text()
        x = (
            self.width()
            - metrics.horizontalAdvance(text)
            - self.kerning * (len(text) - 1)
        ) // 2
        y = (self.height() + metrics.ascent() - metrics.descent()) // 2

        for letter in text:
            painter.drawText(x, y, letter)
            x += metrics.horizontalAdvance(letter) + self.kerning

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            text_rect = self._text_rect()
            if text_rect.contains(event.pos().toPointF()):
                self.copy_to_clipboard()
        super().mousePressEvent(event)

    def _text_rect(self):
        fm = QFontMetrics(self.font())
        text = self.text()
        text_width = fm.horizontalAdvance(text)
        text_height = fm.height()
        rect = self.rect()

        x = (rect.width() - text_width) / 2
        y = (rect.height() + fm.ascent() - fm.descent()) / 2
        return QRectF(x, y - text_height, text_width, text_height)

    def copy_to_clipboard(self):
        from widgets.sequence_widget.current_word_label import CurrentWordLabel
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text())
        parent = self.parent()
        if isinstance(parent, CurrentWordLabel):
            indicator_label = parent.sequence_widget.indicator_label
            indicator_label.show_message(f"'{self.text()}' copied to clipboard")
