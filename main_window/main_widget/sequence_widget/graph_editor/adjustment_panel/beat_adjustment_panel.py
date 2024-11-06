from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QStackedWidget,
    QWidget,
    QSizePolicy,
    QLayout,
)
from data.constants import BLUE, IN, RED
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
        # Set size policies
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(0)
        self._setup_layout()
        self._setup_widgets()

    def _setup_layout(self):
        self.stacked_widget = QStackedWidget(self)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        self.setLayout(self.main_layout)

    def _setup_widgets(self) -> None:
        """Setup the different boxes and widgets for the adjustment panel."""
        self.blue_turns_box: TurnsBox = TurnsBox(self, self.GE_pictograph, BLUE)
        self.red_turns_box: TurnsBox = TurnsBox(self, self.GE_pictograph, RED)
        self.turns_box_set = self._setup_turns_box_set()

        self.blue_ori_picker = OriPickerBox(self, self.GE_pictograph, BLUE)
        self.red_ori_picker = OriPickerBox(self, self.GE_pictograph, RED)
        self.ori_picker_box_set = self._setup_ori_picker_box_set()

        self.placeholder_widget = AdjustmentPanelPlaceHolderText(self)

        self.stacked_widget.addWidget(self.turns_box_set)
        self.stacked_widget.addWidget(self.ori_picker_box_set)
        self.stacked_widget.addWidget(self.placeholder_widget)

    def _setup_ori_picker_box_set(self):
        ori_picker_box_set = QWidget(self)
        ori_picker_layout = QHBoxLayout(ori_picker_box_set)
        ori_picker_layout.setContentsMargins(0, 0, 0, 0)
        ori_picker_layout.setSpacing(0)
        ori_picker_layout.addWidget(self.blue_ori_picker)
        ori_picker_layout.addWidget(self.red_ori_picker)
        self.blue_ori_picker.ori_picker_widget.clickable_ori_label.setText(IN)
        self.red_ori_picker.ori_picker_widget.clickable_ori_label.setText(IN)

        return ori_picker_box_set

    def _setup_turns_box_set(self):
        turns_box_set = QWidget(self)
        turns_layout = QHBoxLayout(turns_box_set)
        turns_layout.setContentsMargins(0, 0, 0, 0)
        turns_layout.setSpacing(0)
        turns_layout.addWidget(self.blue_turns_box)
        turns_layout.addWidget(self.red_turns_box)
        return turns_box_set

    def update_adjustment_panel(self) -> None:
        """Update the panel based on the current pictograph's state."""
        pictograph = (
            self.graph_editor.pictograph_container.GE_pictograph_view.get_current_pictograph()
        )

        if pictograph.is_blank:
            # self.stacked_widget.setCurrentWidget(self.placeholder_widget)
            self.graph_editor.left_stack.setCurrentWidget(
                self.graph_editor.left_stack.widget(0)
            )
            self.graph_editor.right_stack.setCurrentWidget(
                self.graph_editor.right_stack.widget(0)
            )

        elif self.graph_editor.pictograph_container.GE_pictograph_view.is_start_pos:
            self.graph_editor.left_stack.setCurrentWidget(
                self.graph_editor.left_stack.widget(0)
            )
            self.graph_editor.right_stack.setCurrentWidget(
                self.graph_editor.right_stack.widget(0)
            )
        else:
            self.graph_editor.left_stack.setCurrentWidget(
                self.graph_editor.left_stack.widget(1)
            )
            self.graph_editor.right_stack.setCurrentWidget(
                self.graph_editor.right_stack.widget(1)
            )

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
