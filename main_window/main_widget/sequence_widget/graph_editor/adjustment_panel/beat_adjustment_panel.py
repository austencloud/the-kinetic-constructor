from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QStackedWidget, QWidget, QSizePolicy
from data.constants import BLUE, RED, IN
from .adjustment_panel_placeholder_text import AdjustmentPanelPlaceHolderText
from .ori_picker_box.ori_picker_box import OriPickerBox
from .turns_box.turns_box import TurnsBox

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from ..graph_editor import GraphEditor


ORI_WIDGET_INDEX = 0
TURNS_WIDGET_INDEX = 1


class BeatAdjustmentPanel(QFrame):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor)
        self.graph_editor = graph_editor
        self.GE_pictograph = graph_editor.pictograph_container.GE_pictograph
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(0)
        self._initialize_ui()

    def _initialize_ui(self):
        """Initialize layout and widgets with stacked sections for turns and orientation pickers."""
        self.stacked_widget = QStackedWidget(self)

        # Create and set up the main layout without parameters
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Set margins after creation
        self.layout.setSpacing(0)  # Set spacing after creation
        self.layout.addWidget(self.stacked_widget)

        # Set the layout on this panel
        self.setLayout(self.layout)

        # Initialize and configure box pairs
        self.blue_turns_box, self.red_turns_box = TurnsBox(
            self, self.GE_pictograph, BLUE
        ), TurnsBox(self, self.GE_pictograph, RED)
        self.blue_ori_picker, self.red_ori_picker = OriPickerBox(
            self, self.GE_pictograph, BLUE
        ), OriPickerBox(self, self.GE_pictograph, RED)

        for picker in (self.blue_ori_picker, self.red_ori_picker):
            picker.ori_picker_widget.clickable_ori_label.setText(IN)

        # Add box sets to stacked widget
        self.stacked_widget.addWidget(
            self._create_box_set(self.blue_turns_box, self.red_turns_box)
        )
        self.stacked_widget.addWidget(
            self._create_box_set(self.blue_ori_picker, self.red_ori_picker)
        )
        self.stacked_widget.addWidget(AdjustmentPanelPlaceHolderText(self))

    def _create_box_set(self, blue_box, red_box):
        """Creates a container with a horizontal layout for a pair of boxes."""
        box_set = QWidget(self)
        layout = QHBoxLayout(box_set)  # Initialize layout without extra parameters
        layout.setContentsMargins(0, 0, 0, 0)  # Set margins separately
        layout.setSpacing(0)  # Set spacing separately
        layout.addWidget(blue_box)
        layout.addWidget(red_box)
        return box_set

    def update_adjustment_panel(self) -> None:
        """Update the panel view based on the current pictograph state."""
        pictograph_view = self.graph_editor.pictograph_container.GE_pictograph_view
        is_blank = pictograph_view.get_current_pictograph().is_blank
        is_start = pictograph_view.is_start_pos
        self._set_current_stack_widgets(
            ORI_WIDGET_INDEX if is_blank or is_start else TURNS_WIDGET_INDEX
        )

    def _set_current_stack_widgets(self, index):
        """Synchronize left and right stacks to the specified index."""
        for stack in [self.graph_editor.left_stack, self.graph_editor.right_stack]:
            stack.setCurrentWidget(stack.widget(index))

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
        [
            (
                box.header.update_turns_box_header(),
                setattr(box, "matching_motion", motion),
            )
            for box, motion in zip(
                [self.blue_turns_box, self.red_turns_box], [blue_motion, red_motion]
            )
        ]
