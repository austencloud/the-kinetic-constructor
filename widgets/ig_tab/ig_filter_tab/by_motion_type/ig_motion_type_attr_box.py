from typing import TYPE_CHECKING, Dict, List, Optional
from PyQt6.QtGui import QPixmap
from constants import ANTI, DASH, PRO, STATIC
from objects.motion.motion import Motion
from utilities.TypeChecking.TypeChecking import MotionTypes
from widgets.attr_box_widgets.base_attr_box_widget import BaseAttrBoxWidget
from widgets.attr_panel.base_attr_box import BaseAttrBox
from data.letter_engine_data import motion_type_letter_groups
from widgets.ig_tab.ig_filter_tab.by_motion_type.ig_motion_type_header_widget import (
    IGMotionTypeHeaderWidget,
)
from widgets.ig_tab.ig_filter_tab.ig_turns_widget.ig_motion_type_turns_widget import (
    IGMotionTypeTurnsWidget,
)

if TYPE_CHECKING:
    from widgets.ig_tab.ig_filter_tab.by_motion_type.ig_motion_type_attr_panel import (
        IGMotionTypeAttrPanel,
    )
    from objects.pictograph.pictograph import Pictograph

from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout


class IGMotionTypeAttrBox(BaseAttrBox):
    def __init__(
        self,
        attr_panel: "IGMotionTypeAttrPanel",
        pictographs: List["Pictograph"],
        motion_type: MotionTypes,
    ) -> None:
        super().__init__(attr_panel, None)  # Note the None for the single pictograph
        self.attr_panel = attr_panel
        self.motion_type = motion_type
        self.pictographs: Dict[str, Pictograph] = pictographs
        self.font_size = self.width() // 10
        self.attr_box_widgets: List[
            IGMotionTypeTurnsWidget | IGMotionTypeHeaderWidget
        ] = []
        self.combobox_border = 2
        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache
        self.setLayout(self.vbox_layout)
        self._setup_widgets()
        self.update_motion_type_widget_visibility([])

    def update_motion_type_widget_visibility(self, selected_letters: List[str]) -> None:
        """Update the visibility of motion type widgets based on selected letters."""

        if not selected_letters:
            self.show_placeholder_message()
        else:
            motion_types_in_use = set()
            for letter in selected_letters:
                motions = motion_type_letter_groups.get(letter, ())
                motion_types_in_use.update(motions)

            self._update_widget_visibility(PRO, PRO in motion_types_in_use)
            self._update_widget_visibility(ANTI, ANTI in motion_types_in_use)
            self._update_widget_visibility(DASH, DASH in motion_types_in_use)
            self._update_widget_visibility(STATIC, STATIC in motion_types_in_use)

    def show_placeholder_message(self) -> None:
        """Display a placeholder message when no letters are selected."""
        # Remove existing widgets from the layout
        self._clear_layout(self.vbox_layout)

        # Create and configure the placeholder label
        placeholder_label = QLabel(
            "Please select a letter to view motion type adjustments.", self
        )
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_label.setFont(QFont("Arial", 14))
        placeholder_label.setWordWrap(True)

        # Add the placeholder label to the layout
        self.vbox_layout.addWidget(placeholder_label)

    def _clear_layout(
        self, layout: QVBoxLayout, keep_turns_widgets: bool = False
    ) -> None:
        """Remove all widgets from a layout except IGMotionTypeTurnsWidgets if specified."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None and (
                not keep_turns_widgets
                or not isinstance(widget, IGMotionTypeTurnsWidget)
            ):
                widget.hide()

    def _get_widget_by_motion_type(
        self, motion_type: MotionTypes
    ) -> Optional[IGMotionTypeTurnsWidget]:
        """Get a specific motion type widget."""
        for widget in self.attr_box_widgets:
            if widget.motion_type == motion_type:
                return widget

    def _update_widget_visibility(
        self, motion_type: MotionTypes, visible: bool
    ) -> None:
        """Update the visibility of a specific motion type widget."""
        widget = self._get_widget_by_motion_type(motion_type)
        if widget:
            widget.setVisible(visible)

    def add_black_borders(self) -> None:
        self.setStyleSheet(
            f"{self.styleSheet()} border: 1px solid black; border-radius: 0px;"
        )

    def _setup_widgets(self) -> None:  # add common widgets
        self.header_widget = IGMotionTypeHeaderWidget(self, self.motion_type)
        self.turns_widget = IGMotionTypeTurnsWidget(self)
        self.attr_box_widgets.append(self.header_widget)
        self.attr_box_widgets.append(self.turns_widget)

        self.vbox_layout.addWidget(self.header_widget, 1)
        self.vbox_layout.addWidget(self.turns_widget, 2)

    def resize_ig_motion_type_attr_box(self) -> None:
        self.setMinimumWidth(int(self.attr_panel.ig_tab.width() / 6))
        self.setMaximumWidth(int(self.attr_panel.ig_tab.width() / 6))
        self.header_widget.resize_header_widget()
        self.turns_widget.resize_turns_widget()
        self.header_widget.header_label.setFont(QFont("Arial", int(self.width() / 10)))

    def get_pictographs(self) -> List["Pictograph"]:
        return list(self.pictographs.values())

    def update_attr_box(self, motion: Motion) -> None:
        self.turns_widget._update_turnbox(motion.turns)
