# timestamp_label.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from main_window.main_widget.act_tab.editable_label import EditableLabel

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.timestamp_frame import TimestampFrame


class Timestamp(EditableLabel):
    def __init__(self, timestamp_frame: "TimestampFrame", label_text="0:00"):
        super().__init__(timestamp_frame, label_text, align=Qt.AlignmentFlag.AlignLeft)
        self.timestamp_frame = timestamp_frame
        self.act_tab = timestamp_frame.act_tab

    def resize_timestamp(self):
        font_size = int(
            self.timestamp_frame.timestamp_scroll_area.act_sheet.height() // 80
        )
        font = self.label.font()
        font.setPointSize(font_size)
        font.setBold(True)
        self.label.setFont(font)
        self.edit.setFont(font)
