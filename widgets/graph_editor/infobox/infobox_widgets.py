from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QFrame
from settings.string_constants import *
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
    from widgets.graph_editor.infobox.infobox import InfoBox
    from objects.arrow import Arrow
from PyQt6.QtCore import Qt


class InfoBoxFrames:
    def __init__(self, infobox: "InfoBox", graphboard: "GraphBoard") -> None:
        self.infobox = infobox
        self.labels = infobox.labels
        self.graphboard = graphboard

    def setup_frames(self) -> None:
        widget_colors = [BLUE, RED]
        for color in widget_colors:
            attribute_frame = QFrame()
            attribute_frame.setStyleSheet(
                "border: 1px solid black;"
            )  # Add black outlines
            attribute_frame.setObjectName(f"{color}_attribute_frame")
            attribute_frame.setFixedHeight(int(self.infobox.height() / 3))
            attribute_frame.setFixedWidth(int(self.infobox.width() / 3))
            attribute_frame.setContentsMargins(0, 0, 0, 0)

            setattr(self, f"{color}_attribute_frame", attribute_frame)
            attribute_frame.show()

    def construct_attribute_frame(self, color) -> QWidget:
        self.buttons = self.infobox.buttons

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
        self.labels.update_labels(widget, arrow)
        self.infobox.buttons.show_buttons(arrow.color)

    def update_attribute_frames(self) -> None:
        widgets = self.infobox.frames
        for color in [BLUE, RED]:
            arrow = self.graphboard.get_arrow_by_color(color)
            if arrow:
                widget: QFrame = getattr(widgets, f"{color}_attribute_frame")
                self.update_frame_contents(widget, arrow)
                widget.show()
            else:
                widget = getattr(widgets, f"{color}_attribute_frame")
                widget.hide()
