from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QFrame
from settings.string_constants import BLUE, RED
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
    from widgets.graph_editor.infobox.control_panel.control_panel import ControlPanel
    from objects.arrow import Arrow


class InfoBoxFrames:
    """
    Represents the attribute frames in the info box of the graph editor.

    Attributes:
        control_panel (ControlPanel): The control panel associated with the info box.
        labels (Labels): The labels associated with the control panel.
        graphboard (GraphBoard): The graph board associated with the info box.
        blue_attribute_frame (QFrame): The frame for the blue attribute.
        red_attribute_frame (QFrame): The frame for the red attribute.
    """

    def __init__(self, control_panel: "ControlPanel", graphboard: "GraphBoard") -> None:
        self.control_panel = control_panel
        self.labels = control_panel.labels
        self.graphboard = graphboard
        self.blue_attribute_frame: QFrame = None
        self.red_attribute_frame: QFrame = None
        self.setup_frames()

    def setup_frames(self) -> None:
        """
        Set up the attribute frames for the blue and red attributes.
        """
        widget_colors = [BLUE, RED]
        for color in widget_colors:
            attribute_frame = QFrame()
            attribute_frame.setStyleSheet(
                "border: 1px solid black;"
            )  # Add black outlines
            attribute_frame.setObjectName(f"{color}_attribute_frame")
            attribute_frame.setFixedHeight(int(self.control_panel.height() / 3))
            attribute_frame.setFixedWidth(int(self.control_panel.width() / 3))
            attribute_frame.setContentsMargins(0, 0, 0, 0)

            setattr(self, f"{color}_attribute_frame", attribute_frame)
            attribute_frame.show()

    def construct_attribute_frame(self, color) -> QWidget:
        """
        Construct the attribute frame for the given color.

        Args:
            color (str): The color of the attribute frame.

        Returns:
            QWidget: The constructed attribute frame widget.
        """
        self.buttons = self.control_panel.buttons

        (
            motion_type_label,
            rotation_direction_label,
            start_end_label,
            turns_label,
        ) = self.labels.create_attribute_labels()

        start_end_layout = QHBoxLayout()
        start_end_button = getattr(self.buttons, f"swap_start_end_{color}_button")
        start_end_layout.addWidget(start_end_button)
        start_end_layout.addWidget(start_end_label)

        turns_layout = QHBoxLayout()
        decrement_button = getattr(self.buttons, f"decrement_turns_{color}_button")
        increment_button = getattr(self.buttons, f"increment_turns_{color}_button")
        turns_layout.addWidget(decrement_button)
        turns_layout.addWidget(turns_label)
        turns_layout.addWidget(increment_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(motion_type_label)
        main_layout.addWidget(rotation_direction_label)
        main_layout.addWidget(start_end_label)
        main_layout.addLayout(turns_layout)

        info_widget = QWidget()
        info_widget.setLayout(main_layout)
        return info_widget

    def update_frame_contents(self, widget: "QFrame", arrow: "Arrow") -> None:
        """
        Update the contents of the attribute frame with the information from the arrow.

        Args:
            widget (QFrame): The attribute frame widget to update.
            arrow (Arrow): The arrow containing the information.
        """
        self.labels.update_labels(widget, arrow)
        self.control_panel.buttons.show_buttons(arrow.color)

    def update_attribute_frames(self) -> None:
        """
        Update the attribute frames based on the arrows in the graph board.
        """
        widgets = self.control_panel.frames
        for color in [BLUE, RED]:
            arrow = self.graphboard.get_arrow_by_color(color)
            if arrow:
                widget: QFrame = getattr(widgets, f"{color}_attribute_frame")
                self.update_frame_contents(widget, arrow)
                widget.show()
            else:
                widget = getattr(widgets, f"{color}_attribute_frame")
                widget.hide()
