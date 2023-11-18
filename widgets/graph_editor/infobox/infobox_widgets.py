from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QFrame
from settings.string_constants import *
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
    from widgets.infobox.infobox import InfoBox
    from widgets.arrowbox.arrowbox import ArrowBox
    from widgets.propbox.propbox import PropBox
    from widgets.action_buttons_frame import ActionButtonsFrame
    from objects.arrow import Arrow


class InfoBoxWidgets:
    def __init__(self, infobox: "InfoBox", graphboard: "GraphBoard") -> None:
        self.infobox = infobox
        self.labels = infobox.labels

        self.graphboard = graphboard

    def setup_widgets(self) -> None:
        self.blue_attributes_widget = QFrame()
        self.blue_attributes_widget.setFrameShape(QFrame.Shape.Box)
        self.blue_attributes_widget.setFrameShadow(QFrame.Shadow.Sunken)

        self.red_attributes_widget = QFrame()
        self.red_attributes_widget.setFrameShape(QFrame.Shape.Box)
        self.red_attributes_widget.setFrameShadow(QFrame.Shadow.Sunken)

        self.blue_attributes_widget.show()
        self.red_attributes_widget.show()

    def construct_attributes_widget(self, color) -> QWidget:
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

    def update_info_widget_content(self, widget: "QFrame", arrow: "Arrow") -> None:
        self.buttons = self.infobox.buttons
        if widget.layout().count() == 0:
            new_content = self.labels.construct_info_string_label(arrow)
            widget.setLayout(new_content.layout())
            return
        self.labels.update_labels(widget, arrow)
        self.buttons.show_buttons(arrow.color)

    def update_attribute_widgets(self) -> None:
        widgets = self.infobox.widgets
        for color in [BLUE, RED]:
            arrow = self.graphboard.get_arrow_by_color(color)
            if arrow:
                widget = getattr(widgets, f"{color}_attributes_widget")
                self.update_info_widget_content(widget, arrow)
                widget.show()
            else:
                widget = getattr(widgets, f"{color}_attributes_widget")
                widget.hide()
