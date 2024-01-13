from constants import ANTI, DASH, PRO, STATIC
from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import MotionTypes
from data.letter_engine_data import motion_type_letter_combinations
from ....attr_panel.base_attr_panel import BaseAttrPanel
from ..by_motion_type.ig_motion_type_attr_box import IGMotionTypeAttrBox

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

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

    def add_black_borders(self) -> None:
        self.setStyleSheet(
            f"{self.styleSheet()} border: 1px solid black; border-radius: 0px;"
        )
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.setContentsMargins(0, 0, 0, 0)

    def update_motion_type_widget_visibility(self, selected_letters: List[str]) -> None:
        """Update the visibility of motion type widgets based on selected letters."""
        if not selected_letters:
            self.placeholder_label.show()
            for box in self.boxes:
                box.hide()
                box.turns_widget.turns_display.setText("0")
                if hasattr(box.header_widget, "same_button"):
                    box.header_widget.same_button.setChecked(False)
                    box.header_widget.opp_button.setChecked(False)
                    box.header_widget.same_button.setStyleSheet(
                        box.header_widget.get_vtg_dir_button_style(pressed=False)
                    )
                    box.header_widget.opp_button.setStyleSheet(
                        box.header_widget.get_vtg_dir_button_style(pressed=False)
                    )
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
            # if the number of visible boxes is 4,
            for box in self.boxes:
                if len([box for box in self.boxes if box.isVisible()]) == 4:
                    box.setMinimumWidth(int(self.width() / 4 * 0.95))
                    box.setMaximumWidth(int(self.width() / 4 * 0.95))
                elif len([box for box in self.boxes if box.isVisible()]) == 3:
                    box.setMinimumWidth(int(self.width() / 3 * 0.95))
                    box.setMaximumWidth(int(self.width() / 3 * 0.95))
                elif len([box for box in self.boxes if box.isVisible()]) == 2:
                    box.setMinimumWidth(int(self.width() / 2 * 0.95))
                    box.setMaximumWidth(int(self.width() / 2 * 0.95))
                elif len([box for box in self.boxes if box.isVisible()]) == 1:
                    box.setMinimumWidth(int(self.width() * 0.95))
                    box.setMaximumWidth(int(self.width() * 0.95))

    def hide_placeholder_message(self) -> None:
        """Hide the placeholder message."""
        self.placeholder_label.hide()

    def get_turns_for_motion_type(self, motion_type: MotionTypes) -> int:
        for box in self.boxes:
            if box.motion_type == motion_type:
                if box.turns_widget.turns_display.text() in ["0", "1", "2", "3"]:
                    return int(box.turns_widget.turns_display.text())
                elif box.turns_widget.turns_display.text() in ["0.5", "1.5", "2.5"]:
                    return float(box.turns_widget.turns_display.text())

    def resize_ig_motion_type_attr_panel(self) -> None:
        for box in self.boxes:
            box.resize_ig_motion_type_attr_box()
        total_visible_boxes = len([box for box in self.boxes if box.isVisible()])
        for box in self.boxes:
            if total_visible_boxes == 1:
                box.setMinimumWidth(
                    self.width()
                )  # This should allow it to take full width
                box.setMaximumWidth(self.width())
            elif total_visible_boxes == 2:
                box.setMinimumWidth(int(self.width() / 2))
                box.setMaximumWidth(int(self.width() / 2))
            elif total_visible_boxes == 3:
                box.setMinimumWidth(int(self.width() / 3))
                box.setMaximumWidth(int(self.width() / 3))
            elif total_visible_boxes == 4:
                box.setMinimumWidth(int(self.width() / 4))
                box.setMaximumWidth(int(self.width() / 4))

    def reset_turns(self) -> None:
        for box in self.boxes:
            box.turns_widget.turns_display.setText("0")
