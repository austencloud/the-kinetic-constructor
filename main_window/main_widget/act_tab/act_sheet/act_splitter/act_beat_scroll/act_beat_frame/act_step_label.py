# step_label.py
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from .....editable_label import EditableLabel

if TYPE_CHECKING:
    from .act_beat_frame import ActBeatFrame


class ActStepLabel(EditableLabel):
    def __init__(self, act_beat_frame: "ActBeatFrame", label_text=""):
        super().__init__(
            act_beat_frame,
            label_text,
            align=Qt.AlignmentFlag.AlignCenter,
            multi_line=True,
        )
        self.act_beat_frame = act_beat_frame

    def resize_step_label(self):
        self.setFixedHeight(self.act_beat_frame.steps_label_height)
        self.setFixedWidth(self.act_beat_frame.beat_size)
        font_size = self.height() // 4
        font = self.font()
        font.setPointSize(font_size)
        self.setFont(font)
        self.edit.setFont(font)
