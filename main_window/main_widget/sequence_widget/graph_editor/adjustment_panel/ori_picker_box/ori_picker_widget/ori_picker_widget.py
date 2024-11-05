# ori_picker_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QFont, QFontMetrics
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from typing import TYPE_CHECKING
from data.constants import (
    HEX_BLUE,
    HEX_RED,
    IN,
    COUNTER,
    OUT,
    CLOCK,
    START_ORI,
    END_ORI,
    RED,
    BLUE,
)
from main_window.main_widget.sequence_widget.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.ori_setter import OrientationSetter
from main_window.main_widget.sequence_widget.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.ori_text_label import OrientationTextLabel
from .clickable_ori_label import ClickableOriLabel
from .rotate_buttons_widget import RotateButtonsWidget
from .ori_selection_dialog import OriSelectionDialog

if TYPE_CHECKING:
    from ..ori_picker_box import OriPickerBox
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class OriPickerWidget(QWidget):
    """Minimalist widget that displays the orientation controls."""

    ori_adjusted = pyqtSignal(str)

    def __init__(self, ori_picker_box: "OriPickerBox") -> None:
        super().__init__(ori_picker_box)
        self.ori_picker_box = ori_picker_box
        self.color = self.ori_picker_box.color
        self.current_orientation_index = 0
        self.orientations = [IN, COUNTER, OUT, CLOCK]

        self.json_manager = self.ori_picker_box.graph_editor.main_widget.json_manager
        self.json_validation_engine = self.json_manager.ori_validation_engine
        self.option_picker = None
        self.beat_frame = self.ori_picker_box.graph_editor.sequence_widget.beat_frame

        # Instantiate components
        self.orientation_label = OrientationTextLabel(self)
        self.clickable_ori_label = ClickableOriLabel(self)
        self.rotate_buttons_widget = RotateButtonsWidget(self)

        # Instantiate OrientationSetter
        self.ori_setter = OrientationSetter(self)

        # Setup layout
        self._setup_layout()

        # Attach listeners
        self._attach_listeners()

    def _setup_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addStretch(1)
        main_layout.addWidget(self.orientation_label)
        main_layout.addStretch(1)
        main_layout.addWidget(self.clickable_ori_label)
        main_layout.addStretch(1)
        main_layout.addWidget(self.rotate_buttons_widget)
        main_layout.addStretch(1)

    def _attach_listeners(self):
        self.ori_adjusted.connect(self.beat_frame.updater.update_beats_from_json)

    def set_initial_orientation(
        self, start_pos_pictograph: "BasePictograph", color: str
    ) -> None:
        if color == BLUE:
            initial_orientation = start_pos_pictograph.pictograph_dict[
                "blue_attributes"
            ][START_ORI]
        else:
            initial_orientation = start_pos_pictograph.pictograph_dict[
                "red_attributes"
            ][START_ORI]
        self.current_orientation_index = self.orientations.index(initial_orientation)
        self.clickable_ori_label.setText(initial_orientation)



    def resize_ori_picker_widget(self) -> None:
        self.orientation_label.resize_orientation_label()
        self.clickable_ori_label.resize_clickable_ori_label()
        self.rotate_buttons_widget.resize_rotate_buttons_widget()

    def _get_border_color(self) -> str:
        if self.color == RED:
            return HEX_RED
        elif self.color == BLUE:
            return HEX_BLUE
        else:
            return "black"
