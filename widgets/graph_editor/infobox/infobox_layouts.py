from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame
from settings.string_constants import *


class InfoBoxLayouts:
    def __init__(self, infobox, graphboard):
        self.infobox = infobox
        self.graphboard = graphboard
        self.labels = infobox.labels
        self.widgets = infobox.widgets

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

    def setup_layouts(self):
        self.master_layout = QVBoxLayout()
        self.attributes_layouts = {}

        self.setup_top_layout()
        self.setup_bottom_layout()
        self.add_widgets_to_layouts()

        self.infobox.setLayout(self.master_layout)

    def setup_top_layout(self):
        top_layout = QHBoxLayout()
        for color in [BLUE, RED]:
            self.setup_column_layout(color, top_layout)
        self.master_layout.addLayout(top_layout)

    def setup_column_layout(self, color, top_layout):
        column_frame = QFrame()
        column_frame.setFrameShape(QFrame.Shape.Box)
        column_frame.setFrameShadow(QFrame.Shadow.Sunken)
        column_layout = QVBoxLayout()
        header_label = getattr(self.labels, f"{color}_details_label")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        column_layout.addWidget(header_label)
        attributes_buttons_layout = QHBoxLayout()
        self.attributes_layouts[color] = QVBoxLayout()
        self.attributes_layouts[color].setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setup_button_layout()
        attributes_buttons_layout.addLayout(self.button_layout)
        attributes_buttons_layout.addLayout(self.attributes_layouts[color])
        column_layout.addLayout(attributes_buttons_layout)
        column_frame.setLayout(column_layout)
        top_layout.addWidget(column_frame)

    def setup_bottom_layout(self):
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.labels.type_position_label)
        self.master_layout.addLayout(bottom_layout)

    def add_widgets_to_layouts(self):
        self.setup_info_layouts()
        self.setup_attributes_layouts()
        self.add_attributes_widgets_to_layouts()

    def setup_info_layouts(self):
        self.blue_attributes_layout = QVBoxLayout()
        self.red_attributes_layout = QVBoxLayout()
        self.blue_attributes_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.red_attributes_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.blue_attributes_layout.addWidget(self.labels.blue_details_label)
        self.red_attributes_layout.addWidget(self.labels.red_details_label)

    def setup_button_layout(self):
        self.buttons = self.infobox.buttons
        self.button_layout = QVBoxLayout()  # Create a vertical layout for the buttons
        for button_name in self.buttons.button_properties.keys():
            button = getattr(self.buttons, f"{button_name}_button")
            self.button_layout.addWidget(button)  # Add each button to the layout

    def setup_attributes_layouts(self):
        self.setup_attributes_layout(BLUE)
        self.setup_attributes_layout(RED)

    def setup_attributes_layout(self, color):
        attribute_layout = QHBoxLayout()
        buttons_layout = QVBoxLayout()

        for button_name in self.buttons.button_properties.keys():
            if color in button_name and TURNS not in button_name:
                button = getattr(self.buttons, f"{button_name}_button")
                buttons_layout.addWidget(button)

        info_widget_inner = self.widgets.construct_attributes_widget(color)

        attribute_layout.addLayout(buttons_layout)
        attribute_layout.addWidget(info_widget_inner)

        if color == BLUE:
            self.widgets.blue_attributes_widget.setLayout(attribute_layout)
        else:
            self.widgets.red_attributes_widget.setLayout(attribute_layout)

    def add_attributes_widgets_to_layouts(self):
        self.blue_attributes_layout.addWidget(self.widgets.blue_attributes_widget)
        self.red_attributes_layout.addWidget(self.widgets.red_attributes_widget)
        self.attributes_layouts[BLUE].addLayout(self.blue_attributes_layout)
        self.attributes_layouts[RED].addLayout(self.red_attributes_layout)
