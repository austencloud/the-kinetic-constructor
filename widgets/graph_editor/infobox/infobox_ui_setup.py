# import the missing modules
from resources.constants import GRAPHBOARD_SCALE
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
from PyQt6.QtCore import Qt


class InfoboxUISetup:
    def __init__(self, infobox, infobox_manager):
        self.infobox = infobox
        self.infobox_manager = infobox_manager
        self.graphboard_view = infobox.graphboard_view
        self.arrow_manager = self.graphboard_view.arrow_manager
        self.arrow_manipulator = self.arrow_manager.manipulator
        self.helpers = infobox_manager.helpers
        self.labels = infobox_manager.labels
        self.setup_ui_elements()

    def setup_ui_elements(self):
        self.setup_buttons()
        self.setup_labels()
        self.setup_widgets()
        self.create_infobox_buttons()
        self.setup_layouts()
        self.add_widgets_to_layouts()
        self.set_dimensions()

    def setup_buttons(self):
        self.button_properties = {
            "swap_colors": {
                "icon": None,
                "text": "↔",
                "callback": self.arrow_manipulator.swap_colors,
            },
            "swap_motion_type_blue": {
                "icon": "resources/images/icons/swap.jpg",
                "callback": lambda: self.arrow_manipulator.swap_motion_type(
                    self.graphboard_view.get_arrows_by_color("blue"), "blue"
                ),
            },
            "swap_motion_type_red": {
                "icon": "resources/images/icons/swap.jpg",
                "callback": lambda: self.arrow_manipulator.swap_motion_type(
                    self.graphboard_view.get_arrows_by_color("red"), "red"
                ),
            },
            "swap_start_end_blue": {
                "icon": "resources/images/icons/swap.jpg",
                "callback": lambda: self.arrow_manipulator.mirror_arrow(
                    self.graphboard_view.get_arrows_by_color("blue"), "blue"
                ),
            },
            "swap_start_end_red": {
                "icon": "resources/images/icons/swap.jpg",
                "callback": lambda: self.arrow_manipulator.mirror_arrow(
                    self.graphboard_view.get_arrows_by_color("red"), "red"
                ),
            },
            "decrement_turns_blue": {
                "icon": None,
                "text": "-",
                "callback": lambda: self.arrow_manipulator.decrement_turns(
                    self.graphboard_view.get_arrows_by_color("blue"), "blue"
                ),
            },
            "decrement_turns_red": {
                "icon": None,
                "text": "-",
                "callback": lambda: self.arrow_manipulator.decrement_turns(
                    self.graphboard_view.get_arrows_by_color("red"), "red"
                ),
            },
            "increment_turns_blue": {
                "icon": None,
                "text": "+",
                "callback": lambda: self.arrow_manipulator.increment_turns(
                    self.graphboard_view.get_arrows_by_color("blue"), "blue"
                ),
            },
            "increment_turns_red": {
                "icon": None,
                "text": "+",
                "callback": lambda: self.arrow_manipulator.increment_turns(
                    self.graphboard_view.get_arrows_by_color("red"), "red"
                ),
            },
        }

    def create_infobox_buttons(self):
        self.buttons = self.infobox_manager.buttons

        for button_name, properties in self.button_properties.items():
            self.buttons.create_and_set_button(button_name, properties)
            button = getattr(self.infobox, f"{button_name}_button")
            button.setVisible(False)  # Set initial visibility to False

        self.setup_button_layout()

    def setup_button_layout(self):
        self.button_layout = QVBoxLayout()  # Create a vertical layout for the buttons
        for button_name in self.button_properties.keys():
            button = getattr(self.infobox, f"{button_name}_button")
            self.button_layout.addWidget(button)  # Add each button to the layout

    def setup_widgets(self):
        self.blue_info_widget = QFrame()
        self.blue_info_widget.setFrameShape(QFrame.Shape.Box)
        self.blue_info_widget.setFrameShadow(QFrame.Shadow.Sunken)

        self.red_info_widget = QFrame()
        self.red_info_widget.setFrameShape(QFrame.Shape.Box)
        self.red_info_widget.setFrameShadow(QFrame.Shadow.Sunken)

        self.blue_info_widget.setVisible(True)
        self.red_info_widget.setVisible(True)

    def add_widgets_to_layouts(self):
        self.setup_info_layouts()
        self.setup_horizontal_layouts()
        self.add_info_widgets_to_layouts()

    def setup_info_layouts(self):
        self.blue_info_layout = QVBoxLayout()
        self.red_info_layout = QVBoxLayout()
        self.blue_info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.red_info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.blue_info_layout.addWidget(self.blue_details_label)
        self.red_info_layout.addWidget(self.red_details_label)

    def setup_horizontal_layouts(self):
        self.setup_color_horizontal_layout("blue")
        self.setup_color_horizontal_layout("red")

    def setup_color_horizontal_layout(self, color):
        horizontal_layout = QHBoxLayout()
        buttons_layout = QVBoxLayout()

        for button_name in self.button_properties.keys():
            if (
                color in button_name and "turns" not in button_name
            ):  # Exclude the turns buttons
                button = getattr(self.infobox, f"{button_name}_button")
                buttons_layout.addWidget(button)

        # Pass the color as an additional argument to the construct_info_widget method
        info_widget_inner = self.helpers.construct_info_widget(
            self.arrow_manager.attributes.get_graphboard_arrow_attributes_by_color(
                color, self.graphboard_view
            ),
            color,  # Pass the color here
        )

        horizontal_layout.addLayout(buttons_layout)
        horizontal_layout.addWidget(info_widget_inner)

        if color == "blue":
            self.blue_info_widget.setLayout(horizontal_layout)
        else:
            self.red_info_widget.setLayout(horizontal_layout)

    def add_info_widgets_to_layouts(self):
        self.blue_info_layout.addWidget(self.blue_info_widget)
        self.red_info_layout.addWidget(self.red_info_widget)
        self.attributes_layouts["blue"].addLayout(self.blue_info_layout)
        self.attributes_layouts["red"].addLayout(self.red_info_layout)

    def setup_labels(self):
        self.setup_color_label("Left", "blue")
        self.setup_color_label("Right", "red")
        self.type_position_label = self.labels.create_label()

    def setup_color_label(self, text, color):
        label = self.labels.create_label(text, color)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        setattr(self, f"{color}_details_label", label)

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
        header_label = getattr(self, f"{color}_details_label")
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
        bottom_layout.addWidget(self.type_position_label)
        self.master_layout.addLayout(bottom_layout)

    def set_dimensions(self):
        self.infobox.setFixedWidth(int(900 * GRAPHBOARD_SCALE))
        self.infobox.setFixedHeight(int(900 * GRAPHBOARD_SCALE))
