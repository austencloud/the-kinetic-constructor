from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QStackedWidget, QWidget
from data.constants import BLUE, RED
from .adjustment_panel_placeholder_text import AdjustmentPanelPlaceHolderText
from .ori_picker_box.ori_picker_box import OriPickerBox
from .turns_box.turns_box import TurnsBox

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from ..graph_editor import GraphEditor


class BeatAdjustmentPanel(QFrame):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor)
        self.graph_editor = graph_editor
        self.GE_pictograph = graph_editor.pictograph_container.GE_pictograph
        self.initialized = False

        # Create a stacked widget
        self.stacked_widget = QStackedWidget(self)

        # Setup the main layout to take full space and stretch
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.stacked_widget)
        self.setLayout(self.main_layout)

        # Setup widgets and layouts
        self._setup_widgets()
        self._add_widgets_to_stacked_widget()

    def _setup_widgets(self) -> None:
        """Setup the different boxes and widgets for the adjustment panel."""
        self.blue_turns_box: TurnsBox = TurnsBox(self, self.GE_pictograph, BLUE)
        self.red_turns_box: TurnsBox = TurnsBox(self, self.GE_pictograph, RED)
        self.blue_ori_picker = OriPickerBox(self, self.GE_pictograph, BLUE)
        self.red_ori_picker = OriPickerBox(self, self.GE_pictograph, RED)
        self.placeholder_widget = AdjustmentPanelPlaceHolderText(self)

    def _add_widgets_to_stacked_widget(self) -> None:
        """Add the widgets to the QStackedWidget."""

        # Create individual layouts for different states and ensure full width
        turns_widget = QWidget(self)
        turns_layout = QHBoxLayout(turns_widget)
        turns_layout.setContentsMargins(0, 0, 0, 0)
        turns_layout.setSpacing(0)
        turns_layout.addWidget(self.blue_turns_box)
        turns_layout.addWidget(self.red_turns_box)
        # turns_layout.addStretch()
        self.stacked_widget.addWidget(turns_widget)

        ori_picker_widget = QWidget(self)
        ori_picker_layout = QHBoxLayout(ori_picker_widget)
        ori_picker_layout.setContentsMargins(0, 0, 0, 0)
        ori_picker_layout.setSpacing(0)
        ori_picker_layout.addWidget(self.blue_ori_picker)
        ori_picker_layout.addWidget(self.red_ori_picker)
        # ori_picker_layout.addStretch()
        self.stacked_widget.addWidget(ori_picker_widget)

        # Add the placeholder widget to the stacked widget
        self.stacked_widget.addWidget(self.placeholder_widget)

    def update_adjustment_panel(self) -> None:
        """Update the panel based on the current pictograph's state."""
        pictograph = (
            self.graph_editor.pictograph_container.GE_pictograph_view.get_current_pictograph()
        )

        if pictograph.is_blank:
            self.stacked_widget.setCurrentWidget(self.placeholder_widget)
        elif self.graph_editor.pictograph_container.GE_pictograph_view.is_start_pos:
            self.stacked_widget.setCurrentWidget(
                self.stacked_widget.widget(1)
            )  # Ori picker layout
        else:
            self.stacked_widget.setCurrentWidget(
                self.stacked_widget.widget(0)
            )  # Turns boxes layout

    def update_turns_displays(
        self, blue_motion: "Motion", red_motion: "Motion"
    ) -> None:
        """Update the turns displays in the turns boxes."""
        self.blue_turns_box.turns_widget.update_turns_display(
            blue_motion, blue_motion.turns
        )
        self.red_turns_box.turns_widget.update_turns_display(
            red_motion, red_motion.turns
        )

    def update_turns_panel(self, blue_motion: "Motion", red_motion: "Motion") -> None:
        """Update the turns panel with new motion data."""
        self.update_turns_displays(blue_motion, red_motion)
        for box in [self.blue_turns_box, self.red_turns_box]:
            box.header.update_turns_box_header()
            box.matching_motion = blue_motion if box.color == BLUE else red_motion

    def resize_beat_adjustment_panel(self) -> None:
        """Resize the components within the adjustment panel."""
        for turns_box in [self.blue_turns_box, self.red_turns_box]:
            turns_box.resize_turns_box()

        for ori_picker_box in [self.blue_ori_picker, self.red_ori_picker]:
            ori_picker_box.resize_ori_picker_box()

        self.placeholder_widget.resize_adjustment_panel_placeholder_text()
