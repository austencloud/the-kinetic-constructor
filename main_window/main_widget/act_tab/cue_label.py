# timestamp_label.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from main_window.main_widget.act_tab.editable_label import EditableLabel

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.timestamp_frame import TimestampFrame


class CueLabel(EditableLabel):
    def __init__(self, timestamp_frame: "TimestampFrame", label_text=""):
        super().__init__(
            timestamp_frame, label_text, align=Qt.AlignmentFlag.AlignCenter
        )
        self.timestamp_frame = timestamp_frame

    def resize_lyric_label(self):
        font_size = int(
            self.timestamp_frame.timestamp_scroll_area.act_sheet.height() // 100
        )
        font = self.label.font()
        font.setPointSize(font_size)
        font.setBold(True)
        self.label.setFont(font)
        self.edit.setFont(font)
