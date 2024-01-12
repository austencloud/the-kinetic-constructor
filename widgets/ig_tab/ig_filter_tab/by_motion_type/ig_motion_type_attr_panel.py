from constants import ANTI, DASH, PRO, STATIC
from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import MotionTypes
from data.letter_engine_data import motion_type_letter_combinations
from ....attr_panel.base_attr_panel import BaseAttrPanel
from ..by_motion_type.ig_motion_type_attr_box import IGMotionTypeAttrBox

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab


class IGMotionTypeAttrPanel(BaseAttrPanel):
    def __init__(self, ig_tab: "IGTab") -> None:
        super().__init__(ig_tab)
        self.ig_tab = ig_tab

        self.placeholder_label = QLabel(
            "Please select a letter to view motion type adjustments.", self
        )
        self.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder_label.setFont(QFont("Arial", 14))
        self.placeholder_label.setWordWrap(True)
        self.placeholder_label.hide()

        # Add the placeholder label to the layout
        self.setup_layouts()
        self.layout.addWidget(self.placeholder_label)

        self.pro_attr_box = IGMotionTypeAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, PRO
        )
        self.anti_attr_box = IGMotionTypeAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, ANTI
        )
        self.dash_attr_box = IGMotionTypeAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, DASH
        )
        self.static_attr_box = IGMotionTypeAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, STATIC
        )
        self.boxes: List[IGMotionTypeAttrBox] = [
            self.pro_attr_box,
            self.anti_attr_box,
            self.dash_attr_box,
            self.static_attr_box,
        ]
        for box in self.boxes:
            box.hide()
            self.layout.addWidget(box)
        self.placeholder_label.show()
        # self.resize_ig_motion_type_attr_panel()

    def update_motion_type_widget_visibility(self, selected_letters: List[str]) -> None:
        """Update the visibility of motion type widgets based on selected letters."""
        if not selected_letters:
            self.placeholder_label.show()
            for box in self.boxes:
                box.hide()
        else:
            self.hide_placeholder_message()
            motion_types_in_use = set()
            for letter in selected_letters:
                motions = motion_type_letter_combinations.get(letter, ())
                motion_types_in_use.update(motions)

            for box in self.boxes:
                box.setVisible(box.motion_type in motion_types_in_use)
                self.layout.addWidget(box)
                box.resize_ig_motion_type_attr_box()

    def hide_placeholder_message(self) -> None:
        """Hide the placeholder message."""
        self.placeholder_label.hide()

    def get_turns_for_motion_type(self, motion_type: MotionTypes) -> int:
        for box in self.boxes:
            if box.motion_type == motion_type:
                if box.turns_widget.turnbox.currentText() in ["0", "1", "2", "3"]:
                    return int(box.turns_widget.turnbox.currentText())
                elif box.turns_widget.turnbox.currentText() in ["0.5", "1.5", "2.5"]:
                    return float(box.turns_widget.turnbox.currentText())

    def resize_ig_motion_type_attr_panel(self) -> None:
        self.layout.setSpacing(int(self.pro_attr_box.width() / 5))
        for box in self.boxes:
            box.resize_ig_motion_type_attr_box()

    def reset_turns(self) -> None:
        for box in self.boxes:
            box.turns_widget.turnbox.setCurrentText("0")
