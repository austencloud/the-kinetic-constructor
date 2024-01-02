from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING, Callable
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.base_header_widget import (
    BaseHeaderWidget,
)
from widgets.graph_editor_tab.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_attr_box import IGAttrBox
    from widgets.graph_editor_tab.graph_editor_attr_box import (
        GraphEditorAttrBox,
    )
from constants import BLUE, CCW_HANDPATH, CW_HANDPATH, HEX_BLUE, HEX_RED, ICON_DIR, RED
from PyQt6.QtWidgets import QFrame, QVBoxLayout


class IGHeaderWidget(BaseHeaderWidget):
    def __init__(self, attr_box: "IGAttrBox") -> None:
        super().__init__(attr_box)
        self._setup_main_layout()

    def _setup_main_layout(self) -> None:
        super()._setup_main_layout()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addStretch(1)
        header_layout.addWidget(self.header_label)
        header_layout.addStretch(1)
        self.separator = self.create_separator()

        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.separator)

    def _rotate_ccw(self) -> None:
        motion = self.attr_box.pictograph.motions[self.attr_box.color]
        if motion:
            motion.manipulator.rotate_motion(CCW_HANDPATH)

    def _rotate_cw(self) -> None:
        motion = self.attr_box.pictograph.motions[self.attr_box.color]
        if motion:
            motion.manipulator.rotate_motion(CW_HANDPATH)

    def _setup_header_label(self) -> QLabel:
        text = "Left" if self.attr_box.color == BLUE else "Right"
        color_hex = HEX_RED if self.attr_box.color == RED else HEX_BLUE
        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"color: {color_hex}; font-weight: bold;")
        return label

    def resize_header_widget(self) -> None:
        self.separator.setMaximumWidth(
            self.attr_box.width() - self.attr_box.border_width * 2
        )
        self.header_label.setFont(QFont("Arial", int(self.height() / 3)))
        self.setMinimumWidth(self.attr_box.width() - self.attr_box.border_width * 2)
        self.setMaximumWidth(self.attr_box.width() - self.attr_box.border_width * 2)
