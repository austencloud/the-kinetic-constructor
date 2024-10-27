from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextOption, QFontMetrics
from .......editable_label import EditableLabel

if TYPE_CHECKING:
    from ..cue_box import CueBox


class CueLabel(EditableLabel):
    def __init__(self, cue_box: "CueBox", label_text=""):
        super().__init__(
            cue_box,
            label_text,
            align=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
            multi_line=True,
        )
        self.cue_box = cue_box

    def resize_cue_label(self):
        # Set width constraints to match the cue box exactly
        self.setFixedWidth(self.cue_box.width() - 10)  # Small padding for aesthetics
        self.label.setWordWrap(True)
        self.edit.setWordWrapMode(QTextOption.WrapMode.WordWrap)

        # Dynamically adjust font size to fit available space
        font_size = self.calculate_font_size(self.width())
        font = self.label.font()
        font.setPointSize(font_size)
        font.setBold(True)
        self.label.setFont(font)
        self.edit.setFont(font)

    def calculate_font_size(self, width):
        """Calculate appropriate font size based on width constraint."""
        font = self.label.font()
        font_size = font.pointSize()

        while font_size > 5:
            font.setPointSize(font_size)
            metrics = QFontMetrics(font)
            if metrics.horizontalAdvance(self.label.text()) <= width:
                break
            font_size -= 1
        return font_size
