from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QFrame


class InfoboxLayouts:
    def __init__(self, infobox, infobox_manager, graphboard_view, arrow_attributes):
        self.infobox = infobox
        self.infobox_manager = infobox_manager
        self.graphboard_view = graphboard_view
        self.labels = infobox_manager.labels
        self.widgets = infobox_manager.widgets
        self.arrow_attributes = arrow_attributes

    def define_info_layouts(
        self, motion_type_label, rotation_direction_label, start_end_label, turns_label
    ):
        """Define layouts for the info widget."""
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

    def setup_top_layout(self):
        top_layout = QHBoxLayout()
        for color in ["blue", "red"]:
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
        self.setup_horizontal_layouts()
        self.add_info_widgets_to_layouts()

    def setup_info_layouts(self):
        self.blue_info_layout = QVBoxLayout()
        self.red_info_layout = QVBoxLayout()
        self.blue_info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.red_info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.blue_info_layout.addWidget(self.labels.blue_details_label)
        self.red_info_layout.addWidget(self.labels.red_details_label)

    def setup_button_layout(self):
        self.buttons = self.infobox_manager.buttons
        self.button_layout = QVBoxLayout()  # Create a vertical layout for the buttons
        for button_name in self.buttons.button_properties.keys():
            button = getattr(self.infobox, f"{button_name}_button")
            self.button_layout.addWidget(button)  # Add each button to the layout

    def setup_horizontal_layouts(self):
        self.setup_color_horizontal_layout("blue")
        self.setup_color_horizontal_layout("red")

    def setup_color_horizontal_layout(self, color):
        horizontal_layout = QHBoxLayout()
        buttons_layout = QVBoxLayout()

        for button_name in self.buttons.button_properties.keys():
            if (
                color in button_name and "turns" not in button_name
            ):  # Exclude the turns buttons
                button = getattr(self.infobox, f"{button_name}_button")
                buttons_layout.addWidget(button)

        # Pass the color as an additional argument to the construct_info_widget method
        info_widget_inner = self.widgets.construct_info_widget(
            self.arrow_attributes.get_graphboard_arrow_attributes_by_color(
                color, self.graphboard_view
            ),
            color,  # Pass the color here
        )

        horizontal_layout.addLayout(buttons_layout)
        horizontal_layout.addWidget(info_widget_inner)

        if color == "blue":
            self.widgets.blue_info_widget.setLayout(horizontal_layout)
        else:
            self.widgets.red_info_widget.setLayout(horizontal_layout)

    def add_info_widgets_to_layouts(self):
        self.blue_info_layout.addWidget(self.widgets.blue_info_widget)
        self.red_info_layout.addWidget(self.widgets.red_info_widget)
        self.attributes_layouts["blue"].addLayout(self.blue_info_layout)
        self.attributes_layouts["red"].addLayout(self.red_info_layout)