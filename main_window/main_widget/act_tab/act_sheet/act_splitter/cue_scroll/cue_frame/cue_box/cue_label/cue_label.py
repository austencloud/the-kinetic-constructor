# cue_label.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
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
        font_size = int(self.cue_box.cue_frame.cue_scroll.act_sheet.height() // 100)
        font = self.label.font()
        font.setPointSize(font_size)
        font.setBold(True)
        self.label.setFont(font)
        self.edit.setFont(font)
