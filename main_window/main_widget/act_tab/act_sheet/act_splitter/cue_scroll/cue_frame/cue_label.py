# timestamp_label.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from main_window.main_widget.act_tab.editable_label import EditableLabel

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.act_sheet.act_splitter.cue_scroll.cue_frame.cue_box import (
        CueBox,
    )
    from main_window.main_widget.act_tab.act_sheet.act_splitter.cue_scroll.cue_frame.cue_frame import (
        CueFrame,
    )


class CueLabel(EditableLabel):
    def __init__(self, cue_box: "CueBox", label_text=""):
        super().__init__(
            cue_box,
            label_text,
            align=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
        )
        self.cue_box = cue_box

    def resize_lyric_label(self):
        font_size = int(self.cue_box.cue_frame.cue_scroll.act_sheet.height() // 100)
        font = self.label.font()
        font.setPointSize(font_size)
        font.setBold(True)
        self.label.setFont(font)
        self.edit.setFont(font)
