from objects.arrow.arrow import Arrow
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QFrame,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QVBoxLayout,
)
from data.positions_map import positions_map
from resources.constants import GRAPHBOARD_SCALE
from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtGui import QIcon


class InfoFrame(QFrame):
    def __init__(self, main_widget, graphboard_view):
        super().__init__()
        self.setup_variables(main_widget, graphboard_view)
        self.setup_ui_elements()

    def setup_variables(self, main_widget, graphboard_view):
        self.graphboard_view = graphboard_view
        self.remaining_staff = {}
        self.previous_state = None
        self.staff_handler = graphboard_view.staff_handler
        self.letters = main_widget.letters
        self.main_window = main_widget.main_window
        self.arrow_manager = main_widget.arrow_manager
        self.arrow_manipulator = self.arrow_manager.manipulator

    def setup_ui_elements(self):
        self.setup_labels()
        self.setup_layouts()
        self.setLayout(self.grid_layout)
        self.setFixedWidth(int(900 * GRAPHBOARD_SCALE))
        self.setFixedHeight(int(900 * GRAPHBOARD_SCALE))
        self.setup_buttons()

    def setup_buttons(self):
        self.BUTTON_SIZE = 30  # Square button size

        # Create a dictionary to map buttons to their properties
        button_properties = {
            "swap_colors": {"icon": None, "text": "↔", "callback": self.arrow_manipulator.swap_colors},
            "swap_motion_type_blue": {"icon": "resources/images/icons/swap.jpg", "callback": lambda: self.arrow_manipulator.swap_motion_type(self.get_arrows_by_color("blue"), "blue")},
            "swap_motion_type_red": {"icon": "resources/images/icons/swap.jpg", "callback": lambda: self.arrow_manipulator.swap_motion_type(self.get_arrows_by_color("red"), "red")},
            "swap_start_end_blue": {"icon": "resources/images/icons/swap.jpg", "callback": lambda: self.arrow_manipulator.mirror_arrow(self.get_arrows_by_color("blue"), "blue")},
            "swap_start_end_red": {"icon": "resources/images/icons/swap.jpg", "callback": lambda: self.arrow_manipulator.mirror_arrow(self.get_arrows_by_color("red"), "red")},
            "decrement_turns_blue": {"icon": None, "text": "-", "callback": lambda: self.arrow_manipulator.decrement_turns(self.get_arrows_by_color("blue"), "blue")},
            "decrement_turns_red": {"icon": None, "text": "-", "callback": lambda: self.arrow_manipulator.decrement_turns(self.get_arrows_by_color("red"), "red")},
            "increment_turns_blue": {"icon": None, "text": "+", "callback": lambda: self.arrow_manipulator.increment_turns(self.get_arrows_by_color("blue"), "blue")},
            "increment_turns_red": {"icon": None, "text": "+", "callback": lambda: self.arrow_manipulator.increment_turns(self.get_arrows_by_color("red"), "red")}, 
        }

        # Create buttons based on the properties
        for button_name, properties in button_properties.items():
            if properties["icon"]:
                button = QPushButton(QIcon(properties["icon"]), properties.get("text", ""))
            else:
                button = QPushButton(properties.get("text", ""))            
            button.clicked.connect(properties["callback"])
            button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
            setattr(self, f"{button_name}_button", button)

    def get_arrows_by_color(self, color):
        return [item for item in self.graphboard_view.items() if isinstance(item, Arrow) and item.color == color]

    def setup_labels(self):
        self.blue_details_label = self.create_label("Left", "blue")
        self.red_details_label = self.create_label("Right", "red")
        self.type_position_label = self.create_label()

    def create_label(self, text="", color=None):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        if color:
            label.setStyleSheet(f"color: {color}; font-size: 25px; font-weight: bold;")
        return label

    def setup_layouts(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setVerticalSpacing(10)

        header_layout = self.create_horizontal_layout(
            [self.blue_details_label, self.red_details_label]
        )
        self.content_layout = self.create_horizontal_layout()
        type_position_layout = self.create_horizontal_layout([self.type_position_label])

        self.add_widgets_to_grid(
            [header_layout, self.content_layout, type_position_layout]
        )

    def create_horizontal_layout(self, widgets=[]):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        for widget in widgets:
            layout.addWidget(widget)
        return layout

    def add_widgets_to_grid(self, layouts):
        for idx, layout in enumerate(layouts):
            widget = QWidget()
            widget.setLayout(layout)
            if idx == 0:
                widget.setFixedHeight(int(120 * GRAPHBOARD_SCALE))
            elif idx == 2:
                widget.setFixedHeight(int(240 * GRAPHBOARD_SCALE))
            self.grid_layout.addWidget(widget, idx, 0)
            self.grid_layout.setRowStretch(idx, 0 if idx == 0 else 1)

    def update_type_and_position_info(self):
        (
            current_letter,
            current_letter_type,
        ) = self.graphboard_view.info_handler.determine_current_letter_and_type()
        if current_letter and current_letter_type:
            start_end_positions = self.get_start_end_positions()
            if start_end_positions:
                start_position, end_position = start_end_positions

            info_text = f"<center><h1>{current_letter_type}</h1><p style='font-size: 18px; font-family:'Cambria;''>{start_position} → {end_position}</center></p>"
            self.type_position_label.setText(info_text)
        else:
            # Handle cases where the letter or type is not identified
            self.type_position_label.setText("")

    def connect_view(self, graphboard_view):
        self.graphboard_view = graphboard_view

    def get_current_letter(self):
        self.letter = (
            self.graphboard_view.info_handler.determine_current_letter_and_type()[0]
        )
        if self.letter is not None:
            return self.letter

    def update(self):
        self.remaining_staff = {}
        blue_attributes = {}
        red_attributes = {}

        for arrow in [
            item for item in self.graphboard_view.items() if isinstance(item, Arrow)
        ]:
            arrow_dict = arrow.attributes.create_dict_from_arrow(arrow)
            if arrow.color == "blue":
                blue_attributes = arrow_dict
            else:
                red_attributes = arrow_dict

        blue_info_widget = self.construct_info_string_label(blue_attributes)
        red_info_widget = self.construct_info_string_label(red_attributes)

        self.clear_layout(self.content_layout)

        self.content_layout.addWidget(blue_info_widget)
        self.content_layout.addWidget(red_info_widget)

    @staticmethod
    def clear_layout(layout):
        """Removes all widgets from the given layout."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def construct_info_string_label(self, attributes):
        """Constructs a widget with arrow information and associated buttons."""

        # Extract the required values
        motion_type = attributes.get("motion_type", "").capitalize()
        start_location = attributes.get("start_location", "")
        end_location = attributes.get("end_location", "")
        turns = attributes.get("turns", "")
        color = attributes.get("color", "")

        # Create labels
        motion_type_label = QLabel(f"<h1>{motion_type}</h1>")
        start_end_label = QLabel(
            f"<span style='font-weight: bold; font-style: italic; font-size: 20px;'>{start_location.capitalize()} → {end_location.capitalize()}</span>"
        )
        turns_label = QLabel(f"<span style='font-size: 20px;'>{turns}</span>")
        turns_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)  # Set size policy to Fixed


        # Determine which buttons to use based on the color
        swap_motion_type_button = (
            self.swap_motion_type_blue_button
            if color == "blue"
            else self.swap_motion_type_red_button
        )
        swap_start_end_button = (
            self.swap_start_end_blue_button
            if color == "blue"
            else self.swap_start_end_red_button
        )
        decrement_turns_button = (
            self.decrement_turns_blue_button
            if color == "blue"
            else self.decrement_turns_red_button
        )
        increment_turns_button = (
            self.increment_turns_blue_button
            if color == "blue"
            else self.increment_turns_red_button
        )

        # Create layouts for each line
        motion_type_layout = QHBoxLayout()
        motion_type_layout.addWidget(swap_motion_type_button)
        motion_type_layout.addWidget(motion_type_label)

        start_end_layout = QHBoxLayout()
        start_end_layout.addWidget(swap_start_end_button)
        start_end_layout.addWidget(start_end_label)

        turns_layout = QHBoxLayout()
        turns_layout.setSpacing(0)  # Remove spacing between widgets
        turns_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        turns_layout.addWidget(decrement_turns_button)
        turns_layout.addWidget(turns_label)
        turns_layout.addWidget(increment_turns_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(motion_type_layout)
        main_layout.addLayout(start_end_layout)
        main_layout.addLayout(turns_layout)

        # Create a widget to hold the main layout
        info_widget = QWidget()
        info_widget.setLayout(main_layout)

        return info_widget

    def get_start_end_positions(self):
        positions = []
        arrow_items = []
        counter = 1
        start_location_red = None
        end_location_red = None
        start_location_blue = None
        end_location_blue = None
        color_red = None
        color_blue = None
        for item in self.graphboard_view.items():
            if isinstance(item, Arrow):
                arrow_items.append(item)

        for arrow in arrow_items:
            if arrow.color == "red":
                start_location_red = arrow.start_location
                end_location_red = arrow.end_location
                color_red = arrow.color
                counter += 1
            else:  # arrow.color == 'blue'
                start_location_blue = arrow.start_location
                end_location_blue = arrow.end_location
                color_blue = arrow.color

        if (
            start_location_red is not None
            and end_location_red is not None
            and start_location_blue is not None
            and end_location_blue is not None
        ):
            start_key = (start_location_red, color_red, start_location_blue, color_blue)
            end_key = (end_location_red, color_red, end_location_blue, color_blue)
            start_location = positions_map.get(start_key)
            end_location = positions_map.get(end_key)
            positions.append(start_location)
            positions.append(end_location)

        if positions is not None:
            return positions
        else:
            print("no positions returned by get_start_end_positions")
            return None
