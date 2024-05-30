from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QApplication,
    QLineEdit,
)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QFont, QFontMetrics, QMouseEvent

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class CurrentWordLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text())
        parent = self.parent()
        if isinstance(parent, CurrentWordLabel):
            indicator_label = parent.sequence_widget.indicator_label
            indicator_label.show_message(f"'{self.text()}' copied to clipboard")


class CurrentWordLabel(QWidget):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.current_word = None

        self.line_edit = CurrentWordLineEdit(self)

        layout = QHBoxLayout()
        layout.addWidget(self.line_edit)
        self.setLayout(layout)

    def resize_current_word_label(self):
        sequence_widget_width = self.sequence_widget.width()
        font_size = sequence_widget_width // 30
        font = QFont()
        font.setPointSize(int(font_size))
        self.line_edit.setFont(font)

    def set_current_word(self, word: str):
        self.current_word = word
        self.line_edit.setText(word)

    def set_font_color(self, color: str):
        self.line_edit.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: transparent;
                border: none;
                padding-top: 0px;
                padding-bottom: 0px;
                margin: 0px;
                line-height: 1.0em;
                font-family: Georgia;
                font-weight: 600;
                color: {color};
            }}
            """
        )