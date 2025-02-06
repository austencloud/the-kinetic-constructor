# ori_picker_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from typing import TYPE_CHECKING
from data.constants import IN, COUNTER, OUT, CLOCK
from .ori_setter import OrientationSetter
from .ori_text_label import OrientationTextLabel
from .clickable_ori_label import ClickableOriLabel
from .rotate_buttons_widget import RotateButtonsWidget

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.option_picker import OptionPicker
    from ..ori_picker_box import OriPickerBox


class OriPickerWidget(QWidget):
    """Minimalist widget that displays the orientation controls."""

    ori_adjusted = pyqtSignal(str)
    current_orientation_index = 0
    orientations = [IN, COUNTER, OUT, CLOCK]
    option_picker: "OptionPicker" = None

    def __init__(self, ori_picker_box: "OriPickerBox") -> None:
        super().__init__(ori_picker_box)
        self.ori_picker_box = ori_picker_box
        self.color = self.ori_picker_box.color

        self.json_manager = self.ori_picker_box.graph_editor.main_widget.json_manager
        self.json_validation_engine = self.json_manager.ori_validation_engine
        self.beat_frame = self.ori_picker_box.graph_editor.sequence_widget.beat_frame

        self.orientation_text_label = OrientationTextLabel(self)
        self.clickable_ori_label = ClickableOriLabel(self)
        self.rotate_buttons_widget = RotateButtonsWidget(self)
        self.ori_setter = OrientationSetter(self)

        self._setup_layout()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        widgets = [
            self.orientation_text_label,
            self.clickable_ori_label,
            self.rotate_buttons_widget,
        ]

        for widget in widgets:
            self.layout.addStretch(1)
            self.layout.addWidget(widget)
        self.layout.addStretch(1)
