from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame
from settings.string_constants import RED, BLUE, TURNS
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
    from widgets.graph_editor.infobox.infobox import InfoBox

from PyQt6.QtWidgets import QLabel
from utilities.TypeChecking.TypeChecking import Color
from widgets.graph_editor.infobox.infobox_buttons import InfoBoxButtons
from widgets.graph_editor.infobox.infobox_frames import InfoBoxFrames
from widgets.graph_editor.infobox.infobox_labels import InfoBoxLabels


class ControlPanel(QFrame):
    def __init__(self, infobox: "InfoBox", graphboard: "GraphBoard") -> None:
        super().__init__()
        self.infobox = infobox
        self.graphboard = graphboard

        self.buttons = InfoBoxButtons(self, graphboard)
        self.labels = InfoBoxLabels(self, graphboard)
        self.frames = InfoBoxFrames(self, graphboard)

        self.setup_layouts()

    def update(self) -> None:
        self.frames.update()
        self.labels.update_type_and_position_label()

    def define_info_layouts(
        self, motion_type_label, rotation_direction_label, start_end_label, turns_label
    ):
        motion_type_layout = QHBoxLayout()
        motion_type_layout.addWidget(motion_type_label)
        motion_type_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_end_layout = QHBoxLayout()
        start_end_layout.addWidget(start_end_label)
        start_end_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        rotation_direction_layout = QHBoxLayout()
        rotation_direction_layout.addWidget(rotation_direction_label)
        rotation_direction_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        turns_layout = QHBoxLayout()
        turns_layout.addWidget(turns_label)
        turns_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addLayout(motion_type_layout)
        main_layout.addLayout(start_end_layout)
        main_layout.addLayout(turns_layout)

        return main_layout

    def setup_layouts(self) -> None:
        self.master_layout = QHBoxLayout()
        self.attributes_layouts: Dict[Color, QVBoxLayout] = {}
        self.setup_bottom_layout()
        for color in [BLUE, RED]:
            self.setup_column_layout(color)
        self.add_widgets_to_layouts()
        self.infobox.setLayout(self.master_layout)

    def setup_column_layout(self, color: Color) -> None:
        column_frame = QFrame()
        column_frame.setFrameShape(QFrame.Shape.Box)
        column_frame.setFrameShadow(QFrame.Shadow.Sunken)
        column_layout = QVBoxLayout()
        header_label_frame = QFrame()
        header_label_frame.setFrameShape(QFrame.Shape.Box)
        header_label_frame.setFrameShadow(QFrame.Shadow.Sunken)
        header_label_frame.setLineWidth(1)
        header_label_frame.setContentsMargins(0, 0, 0, 0)
        header_label_frame.setStyleSheet("border: 1px solid black;")
        header_layout = QHBoxLayout()

        header_label: QLabel = getattr(self.labels, f"{color}_details_label")
        header_label.setContentsMargins(0, 0, 0, 0)
        header_layout.addWidget(header_label)
        header_label_frame.setLayout(header_layout)

        attributes_buttons_layout = QHBoxLayout()
        self.attributes_layouts[color] = QVBoxLayout()
        self.attributes_layouts[color].setAlignment(Qt.AlignmentFlag.AlignCenter)
        attributes_buttons_layout.addLayout(self.buttons.button_layout)
        attributes_buttons_layout.addLayout(self.attributes_layouts[color])
        column_layout.addWidget(header_label_frame)
        column_layout.addLayout(attributes_buttons_layout)
        column_frame.setLayout(column_layout)
        self.master_layout.addWidget(column_frame)

    def setup_bottom_layout(self) -> None:
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.labels.type_position_label)
        self.master_layout.addLayout(bottom_layout)

    def add_widgets_to_layouts(self) -> None:
        self.setup_info_layouts()
        self.setup_attributes_layouts()
        self.add_attributes_widgets_to_layouts()

    def setup_info_layouts(self) -> None:
        self.blue_attributes_layout = QVBoxLayout()
        self.red_attributes_layout = QVBoxLayout()
        self.blue_attributes_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.red_attributes_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.blue_attributes_layout.addWidget(self.labels.blue_details_label)
        self.red_attributes_layout.addWidget(self.labels.red_details_label)

    def setup_attributes_layouts(self) -> None:
        self.setup_attributes_layout(BLUE)
        self.setup_attributes_layout(RED)

    def setup_attributes_layout(self, color) -> None:
        attribute_layout = QHBoxLayout()
        buttons_layout = QVBoxLayout()

        for button_name in self.buttons.button_properties.keys():
            if color in button_name and TURNS not in button_name:
                button = getattr(self.buttons, f"{button_name}_button")
                buttons_layout.addWidget(button)

        info_widget_inner = self.frames.construct_attribute_frame(color)

        attribute_layout.addLayout(buttons_layout)
        attribute_layout.addWidget(info_widget_inner)

        if color == BLUE:
            self.frames.blue_attribute_frame.setLayout(attribute_layout)
        else:
            self.frames.red_attribute_frame.setLayout(attribute_layout)

    def add_attributes_widgets_to_layouts(self) -> None:
        self.blue_attributes_layout.addWidget(self.frames.blue_attribute_frame)
        self.red_attributes_layout.addWidget(self.frames.red_attribute_frame)
        self.attributes_layouts[BLUE].addLayout(self.blue_attributes_layout)
        self.attributes_layouts[RED].addLayout(self.red_attributes_layout)
