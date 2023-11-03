from PyQt6.QtWidgets import (
    QLabel,
    QFrame,
    QGridLayout,
    QVBoxLayout,
)
from resources.constants import GRAPHBOARD_SCALE
import logging
from widgets.graph_editor.infobox.infobox_button_manager import InfoboxButtonManager
from widgets.graph_editor.infobox.infobox_helpers import InfoboxHelpers

logging.basicConfig(
    filename="tka.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


class Infobox(QFrame):
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
        self.button_manager = InfoboxButtonManager(
            self, self.arrow_manipulator, self.graphboard_view
        )
        self.helpers = InfoboxHelpers()
        self.setup_labels()
        self.setup_layouts()
        self.setLayout(self.grid_layout)
        self.set_dimensions()
        self.button_manager.setup_buttons()
        logging.debug("InfoFrame setup_ui_elements")

        # Pre-create widgets
        self.blue_info_widget = self.helpers.construct_info_string_label({})
        self.red_info_widget = self.helpers.construct_info_string_label({})

        # Create separate layouts for blue and red info widgets
        self.blue_info_layout = QVBoxLayout()
        self.red_info_layout = QVBoxLayout()

        # Add the header labels to their respective layouts
        self.blue_info_layout.addWidget(self.blue_details_label)
        self.red_info_layout.addWidget(self.red_details_label)

        # Add the widgets to their respective layouts
        self.blue_info_layout.addWidget(self.blue_info_widget)
        self.red_info_layout.addWidget(self.red_info_widget)

        # Add the layouts to the main content layout
        self.content_layout.addLayout(self.blue_info_layout)
        self.content_layout.addLayout(self.red_info_layout)

        # Initially hide them
        self.blue_info_widget.setVisible(False)
        self.red_info_widget.setVisible(False)

    def set_dimensions(self):
        self.setFixedWidth(int(900 * GRAPHBOARD_SCALE))
        self.setFixedHeight(int(900 * GRAPHBOARD_SCALE))

    def setup_labels(self):
        self.blue_details_label = self.helpers.create_label("Left", "blue")
        self.red_details_label = self.helpers.create_label("Right", "red")
        self.type_position_label = self.helpers.create_label()

    def setup_layouts(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setVerticalSpacing(10)

        header_layout = self.helpers.create_horizontal_layout(
            [self.blue_details_label, self.red_details_label]
        )
        self.content_layout = self.helpers.create_horizontal_layout()
        type_position_layout = self.helpers.create_horizontal_layout(
            [self.type_position_label]
        )

        self.helpers.add_widgets_to_grid(
            self.grid_layout, [header_layout, self.content_layout, type_position_layout]
        )

    def update_type_and_position_info(self):
        (
            current_letter,
            current_letter_type,
        ) = self.graphboard_view.info_handler.determine_current_letter_and_type()
        if current_letter and current_letter_type:
            start_end_positions = self.helpers.get_start_end_positions(self.graphboard_view)
            if start_end_positions:
                start_position, end_position = start_end_positions

            info_text = f"<center><h1>{current_letter_type}</h1><p style='font-size: 18px; font-family:'Cambria;''>{start_position} → {end_position}</center></p>"
            self.type_position_label.setText(info_text)
        else:
            # Handle cases where the letter or type is not identified
            self.type_position_label.setText("")

    def get_current_letter(self):
        self.letter = (
            self.graphboard_view.info_handler.determine_current_letter_and_type()[0]
        )
        if self.letter is not None:
            return self.letter

    def update(self):
        blue_attributes = {}
        red_attributes = {}

        blue_arrows = self.button_manager.get_arrows_by_color("blue")
        red_arrows = self.button_manager.get_arrows_by_color("red")

        # Check if there are blue arrows on the board
        if blue_arrows:
            blue_attributes = blue_arrows[0].attributes.create_dict_from_arrow(
                blue_arrows[0]
            )
            self.update_info_widget_content(self.blue_info_widget, blue_attributes)
            self.blue_info_widget.setVisible(True)
        else:
            self.blue_info_widget.setVisible(False)

        # Check if there are red arrows on the board
        if red_arrows:
            red_attributes = red_arrows[0].attributes.create_dict_from_arrow(
                red_arrows[0]
            )
            self.update_info_widget_content(self.red_info_widget, red_attributes)
            self.red_info_widget.setVisible(True)
        else:
            self.red_info_widget.setVisible(False)

    def update_info_widget_content(self, widget, attributes):
        # If the widget doesn't have any children, initialize it
        if widget.layout().count() == 0:
            new_content = self.construct_info_string_label(attributes)
            widget.setLayout(new_content.layout())
            return

        # Otherwise, update the existing content
        motion_type_label = widget.findChild(QLabel, "motion_type_label")
        start_end_label = widget.findChild(QLabel, "start_end_label")
        turns_label = widget.findChild(QLabel, "turns_label")

        # Extract the required values
        motion_type = attributes.get("motion_type", "").capitalize()
        start_location = attributes.get("start_location", "")
        end_location = attributes.get("end_location", "")
        turns = attributes.get("turns", "")

        # Update labels
        motion_type_label.setText(f"<h1>{motion_type}</h1>")
        if motion_type in ["Pro", "Anti", "Static"]:
            start_end_label.setText(
                f"<span style='font-weight: bold; font-style: italic; font-size: 20px;'>{start_location.capitalize()} → {end_location.capitalize()}</span>"
            )
        elif motion_type == "":
            start_end_label.setText(f"")
        turns_label.setText(f"<span style='font-size: 20px;'>{turns}</span>")

        # Determine which buttons to use based on the color
        color = attributes.get("color", "")
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

        # Make the buttons visible
        swap_motion_type_button.setVisible(True)
        swap_start_end_button.setVisible(True)
        decrement_turns_button.setVisible(True)
        increment_turns_button.setVisible(True)
