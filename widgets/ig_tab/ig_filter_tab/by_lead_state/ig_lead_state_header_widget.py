from PyQt6.QtWidgets import QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING
from utilities.TypeChecking.TypeChecking import LeadStates

from widgets.attr_box_widgets.base_header_widget import BaseHeaderWidget

if TYPE_CHECKING:
    from widgets.ig_tab.ig_filter_tab.by_lead_state.ig_lead_state_attr_box import (
        IGLeadStateAttrBox,
    )
from constants import (
    LEADING,
    TRAILING,
)


class IGLeadStateHeaderWidget(BaseHeaderWidget):
    def __init__(self, attr_box: "IGLeadStateAttrBox", lead_state: LeadStates) -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.lead_state = lead_state
        self.header_label = self._setup_header_label()
        self.separator = self.create_separator()
        self._setup_layout()

    def _setup_layout(self) -> None:
        super()._setup_layout()
        header_layout = QHBoxLayout()
        header_layout.addStretch(1)
        header_layout.addWidget(self.header_label)
        header_layout.addStretch(1)
        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.separator)

    def _setup_dash_static_layout(self) -> None:
        super()._setup_layout()
        header_layout = QHBoxLayout()
        header_layout.addStretch(1)
        header_layout.addWidget(self.header_label)
        header_layout.addStretch(1)
        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.separator)

    def _setup_header_label(self) -> QLabel:
        text = ""
        font_size = 30
        font_weight = "bold"

        if self.lead_state == LEADING:
            text = "Leading"
        elif self.lead_state == TRAILING:
            text = "Trailing"

        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"font-size: {font_size}px; font-weight: {font_weight};")
        return label
