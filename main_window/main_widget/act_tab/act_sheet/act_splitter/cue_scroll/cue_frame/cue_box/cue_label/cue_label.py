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
        width = int(self.cue_box.cue_frame.cue_scroll.act_sheet.width() // 9)
        self.setFixedWidth(width)
        self.label.setFixedWidth(width)
        self.label.setWordWrap(True)
        self.edit.setFixedWidth(width)
        self.edit.setWordWrapMode(QTextOption.WrapMode.WordWrap)

        # Reapply your margins
        margin = int(self.cue_box.height() // 8)
        self.apply_styles(margin)

        # Dynamically adjust font size based on width
        font_size = self.calculate_font_size(width)
        font = self.label.font()
        font.setPointSize(font_size)
        font.setBold(True)
        self.label.setFont(font)
        self.edit.setFont(font)

    def calculate_font_size(self, width):
        """Calculate font size based on width without expanding height."""
        font = self.label.font()
        font_size = font.pointSize()

        while font_size > 5:
            font.setPointSize(font_size)
            metrics = QFontMetrics(font)
            if metrics.boundingRect(self.label.text()).width() <= width:
                break
            font_size -= 1
        return font_size

    def _show_edit(self, event=None) -> None:
        super()._show_edit(event)
        self.edit.setFixedWidth(self.width() - 10)
