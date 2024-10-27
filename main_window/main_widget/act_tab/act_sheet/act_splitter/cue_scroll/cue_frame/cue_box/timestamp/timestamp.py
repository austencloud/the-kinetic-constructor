from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from .......editable_label import EditableLabel

if TYPE_CHECKING:
    from ..cue_box import CueBox

from typing import TYPE_CHECKING
from .timestamp_line_edit import TimestampLineEdit  # Import the custom line edit

if TYPE_CHECKING:
    from ..cue_box import CueBox


class Timestamp(EditableLabel):
    def __init__(self, cue_box: "CueBox", label_text="0:00"):
        super().__init__(
            cue_box, label_text, align=Qt.AlignmentFlag.AlignLeft, multi_line=False
        )
        self.cue_box = cue_box

        # Replace the default QLineEdit with TimestampLineEdit for auto-formatting
        self.edit = TimestampLineEdit(label_text)
        self.layout.addWidget(self.edit)  # Add it to the layout

    def resize_timestamp(self):
        font_size = int(self.cue_box.cue_frame.cue_scroll.act_sheet.height() // 80)
        font = self.label.font()
        font.setPointSize(font_size)
        font.setBold(True)
        self.label.setFont(font)
        self.edit.setFont(font)
