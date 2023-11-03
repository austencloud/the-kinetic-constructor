# import the missing modules
from resources.constants import GRAPHBOARD_SCALE
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
from PyQt6.QtCore import Qt

class InfoboxUISetup:
    def __init__(self, infobox, infobox_manager):
        self.infobox = infobox
        self.infobox_manager = infobox_manager
        self.helpers = infobox_manager.helpers
        self.graphboard_view = infobox.graphboard_view
        self.arrow_manager = self.graphboard_view.arrow_manager
        self.arrow_manipulator = self.arrow_manager.manipulator
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
        self.button_factory = self.infobox_manager.button_factory
        
        for button_name, properties in self.button_properties.items():
            self.button_factory.create_and_set_button(button_name, properties)
            button = getattr(self.infobox, f"{button_name}_button")
            button.setVisible(False)  # Set initial visibility to False
            
        self.setup_button_layout()

    def setup_button_layout(self):
        self.button_layout = QVBoxLayout()  # Create a vertical layout for the buttons
        for button_name in self.button_properties.keys():
            button = getattr(self.infobox, f"{button_name}_button")
            self.button_layout.addWidget(button)  # Add each button to the layout

        
    def setup_widgets(self):
        blue_attributes = self.arrow_manager.attributes.get_graphboard_arrow_attributes_by_color("blue", self.graphboard_view)
        red_attributes = self.arrow_manager.attributes.get_graphboard_arrow_attributes_by_color("red", self.graphboard_view)
        
        self.blue_info_widget = self.helpers.construct_info_widget(blue_attributes)
        self.red_info_widget = self.helpers.construct_info_widget(red_attributes)
        self.blue_info_widget.setVisible(True)
        self.red_info_widget.setVisible(True)



    def add_widgets_to_layouts(self):
        self.blue_info_layout = QVBoxLayout()
        self.red_info_layout = QVBoxLayout()

        self.blue_info_layout.addWidget(self.blue_details_label)
        self.red_info_layout.addWidget(self.red_details_label)

        self.blue_info_layout.addWidget(self.blue_info_widget)
        self.red_info_layout.addWidget(self.red_info_widget)

        self.attributes_layouts["blue"].addLayout(self.blue_info_layout)
        self.attributes_layouts["red"].addLayout(self.red_info_layout)


    def setup_labels(self):
        self.blue_details_label = self.helpers.create_label("Left", "blue")
        self.red_details_label = self.helpers.create_label("Right", "red")
        self.type_position_label = self.helpers.create_label()

    def setup_layouts(self):
        self.master_layout = QVBoxLayout()
        self.attributes_layouts = {}  # Dictionary to store layouts for each color
        
        top_layout = QHBoxLayout()
        for color in ["blue", "red"]:
            column_frame = QFrame()
            column_frame.setFrameShape(QFrame.Shape.Box)
            column_frame.setFrameShadow(QFrame.Shadow.Sunken)
            
            column_layout = QVBoxLayout()
            header_label = getattr(self, f"{color}_details_label")
            column_layout.addWidget(header_label)
            
            attributes_buttons_layout = QHBoxLayout()
            
            self.attributes_layouts[color] = QVBoxLayout()  # Define layout for each color
            self.attributes_layouts[color].setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            buttons_layout = QVBoxLayout()
            for button_name in self.button_properties.keys():
                if color in button_name:
                    button = getattr(self.infobox, f"{button_name}_button")
                    buttons_layout.addWidget(button)
            
            attributes_buttons_layout.addLayout(buttons_layout)
            attributes_buttons_layout.addLayout(self.attributes_layouts[color])  # Use the layout from the dictionary
            
            column_layout.addLayout(attributes_buttons_layout)
            column_frame.setLayout(column_layout)
            top_layout.addWidget(column_frame)
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.type_position_label)
        
        self.master_layout.addLayout(top_layout)
        self.master_layout.addLayout(bottom_layout)
        


        
    def set_dimensions(self):
        self.infobox.setFixedWidth(int(900 * GRAPHBOARD_SCALE))
        self.infobox.setFixedHeight(int(900 * GRAPHBOARD_SCALE))
