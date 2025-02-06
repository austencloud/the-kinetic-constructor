from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QStackedWidget, QWidget, QSizePolicy
from data.constants import BLUE, RED, IN
from .adjustment_panel_placeholder_text import AdjustmentPanelPlaceHolderText
from .ori_picker_box.ori_picker_box import OriPickerBox
from .turns_box.turns_box import TurnsBox

if TYPE_CHECKING:
    from ..graph_editor import GraphEditor


ORI_WIDGET_INDEX = 0
TURNS_WIDGET_INDEX = 1


class BeatAdjustmentPanel(QFrame):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor)
        self.graph_editor = graph_editor
        self.GE_pictograph = graph_editor.pictograph_container.GE_pictograph
        self.beat_frame = self.graph_editor.sequence_widget.beat_frame
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
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
        layout = QHBoxLayout(box_set)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(blue_box)
        layout.addWidget(red_box)
        return box_set

    def update_adjustment_panel(self) -> None:
        """Update the panel view based on the current pictograph state."""
        view = self.graph_editor.pictograph_container.GE_view
        is_blank = view.get_current_pictograph().is_blank
        widget_index = (
            ORI_WIDGET_INDEX if is_blank or view.is_start_pos else TURNS_WIDGET_INDEX
        )
        self._set_current_stack_widgets(widget_index)
        self.update_turns_displays()
        self.update_rot_dir_buttons()

    def update_rot_dir_buttons(self) -> None:
        """Update the rotation direction buttons based on the current pictograph state."""
        reference_beat = self.beat_frame.get.currently_selected_beat_view()
        if reference_beat:
            blue_motion = reference_beat.beat.blue_motion
            red_motion = reference_beat.beat.red_motion

            blue_rot_dir = blue_motion.prop_rot_dir
            red_rot_dir = red_motion.prop_rot_dir

            self.blue_turns_box.prop_rot_dir_button_manager._update_button_states(
                blue_rot_dir
            )
            self.red_turns_box.prop_rot_dir_button_manager._update_button_states(
                red_rot_dir
            )

    def _set_current_stack_widgets(self, index):
        """Synchronize left and right stacks to the specified index."""
        for stack in [self.graph_editor.left_stack, self.graph_editor.right_stack]:
            stack.setCurrentWidget(stack.widget(index))

    def update_turns_displays(self) -> None:
        """Update the turns displays in the turns boxes."""
        blue_motion = self.GE_pictograph.blue_motion
        red_motion = self.GE_pictograph.red_motion
        for box, motion in zip(
            [self.blue_turns_box, self.red_turns_box], [blue_motion, red_motion]
        ):
            box.turns_widget.update_turns_display(motion, motion.turns)

    def update_turns_panel(self) -> None:
        """Update the turns panel with new motion data."""
        blue_motion = self.GE_pictograph.blue_motion
        red_motion = self.GE_pictograph.red_motion
        self.update_turns_displays()
        [
            (
                box.header.update_turns_box_header(),
                setattr(box, "matching_motion", motion),
            )
            for box, motion in zip(
                [self.blue_turns_box, self.red_turns_box], [blue_motion, red_motion]
            )
        ]
