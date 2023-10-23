from objects.arrow import Arrow
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget
from data.positions_map import positions_map

from settings import GRAPHBOARD_SCALE
from data.start_end_location_mapping import start_end_location_mapping

class GraphboardInfoFrame(QFrame):

    def __init__(self, main_widget, graphboard_view):
        super().__init__()
        self.setup_variables(main_widget, graphboard_view)
        self.setup_ui_elements()

    def setup_variables(self, main_widget, graphboard_view):
        self.graphboard_view = graphboard_view
        self.remaining_staff = {}
        self.previous_state = None
        self.staff_manager = graphboard_view.staff_manager
        self.letters = main_widget.letters
        self.main_window = main_widget.main_window

    def setup_ui_elements(self):
        self.setup_labels()
        self.setup_layouts()
        self.setLayout(self.grid_layout)
        self.setFixedWidth(int(900 * GRAPHBOARD_SCALE))
        self.setFixedHeight(int(900 * GRAPHBOARD_SCALE))

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

        header_layout = self.create_horizontal_layout([self.blue_details_label, self.red_details_label])
        self.content_layout = self.create_horizontal_layout()
        type_position_layout = self.create_horizontal_layout([self.type_position_label])

        self.add_widgets_to_grid([header_layout, self.content_layout, type_position_layout])

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
        # Determine the current letter and its type
        current_letter, current_letter_type = self.graphboard_view.info_manager.determine_current_letter_and_type()

        # Check if the letter and type were successfully retrieved
        if current_letter and current_letter_type:
            # Determine the start and end positions based on the current state
            start_end_positions = self.get_start_end_locations()
            if start_end_positions:
                start_position, end_position = start_end_positions


            # Now that you have new type, letter, and position information, you can update the relevant label.
            info_text = f"<center><h2>{current_letter_type}</h2><p style='font-size: 18px; font-family:'Cambria;''>{start_position} → {end_position}</center></p>"
            self.type_position_label.setText(info_text)
        else:
            # Handle cases where the letter or type is not identified
            self.type_position_label.setText("")
            
    def connect_view(self, graphboard_view):
        self.graphboard_view = graphboard_view

    def get_current_letter(self):
        self.letter = self.graphboard_view.info_manager.determine_current_letter_and_type()[0]
        if self.letter is not None:
            return self.letter
    
   
    def update(self):
        self.remaining_staff = {}  # Reset the remaining staff info

        # Create placeholders for arrow attributes to ensure alignment
        blue_attributes = {}
        red_attributes = {}

        # Now, we can construct the initial text for the labels since we have initialized the attributes.
        blue_text = ""
        red_text = ""

        # Process the arrows and construct detailed information
        for arrow in [item for item in self.graphboard_view.items() if isinstance(item, Arrow)]:
            
            if not arrow.is_ghost:
                arrow.set_attributes_from_filename()  # Ensure the attributes are up-to-date

            # Update the respective attribute dictionaries
            attributes_dict = blue_attributes if arrow.color == 'blue' else red_attributes if arrow.color == 'red' else None



    # Use the dictionary to update arrow locations
            if arrow.quadrant in start_end_location_mapping:
                if arrow.rotation_direction in start_end_location_mapping[arrow.quadrant]:
                    if arrow.motion_type in start_end_location_mapping[arrow.quadrant][arrow.rotation_direction]:
                        arrow.start_location, arrow.end_location = start_end_location_mapping[arrow.quadrant][arrow.rotation_direction][arrow.motion_type]


        # Construct information strings ensuring the values (not keys) are bold and aligned
        blue_info_label = self.construct_info_string_label(blue_attributes)
        red_info_label = self.construct_info_string_label(red_attributes)

        # Append arrow information to the section text
        blue_text += blue_info_label.text()
        red_text += red_info_label.text()

        self.clear_layout(self.content_layout)

        self.content_layout.addWidget(blue_info_label)
        self.content_layout.addWidget(red_info_label)

        # Now that you have new type, letter, and position information, you can update the relevant label.
        self.update_type_and_position_info()

        # Inform the graphboard graphboard_view about the current letter
        self.graphboard_view.update_letter(self.graphboard_view.info_manager.determine_current_letter_and_type()[0])


        # Update the staffs on the graphboard based on the new state
        self.staff_manager.update_graphboard_staffs(self.graphboard_view.scene())

    @staticmethod
    def clear_layout(layout):
        """Removes all widgets from the given layout."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def construct_info_string_label(self, attributes):
        """Constructs a formatted string for arrow information with aligned values."""
        info_strings = []
        for key, value in attributes.items():
            if value:  # Check if the value is not an empty string
                # Make keys italic and values bold, and both black in color
                info_strings.append(f"<span style='font-style: italic; color: black;'>{key}:</span> <span style='font-weight: bold; color: black;'>{value}</span><br>")

        # Combine all attribute strings and wrap them in a paragraph with a specific font size
        return QLabel("<p style='font-size: 18px; text-align: left;'>" + "".join(info_strings) + "</p>")
    
    def get_start_end_locations(self):
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
            if arrow.color == 'red':
                start_location_red = arrow.start_location
                end_location_red = arrow.end_location
                color_red = arrow.color
                counter += 1
            else: # arrow.color == 'blue'
                start_location_blue = arrow.start_location
                end_location_blue = arrow.end_location
                color_blue = arrow.color

        if start_location_red is not None and end_location_red is not None and start_location_blue is not None and end_location_blue is not None:
            start_key = (start_location_red, color_red, start_location_blue, color_blue)
            end_key = (end_location_red, color_red, end_location_blue, color_blue)
            start_location = positions_map.get(start_key)
            end_location = positions_map.get(end_key)
            positions.append(start_location)
            positions.append(end_location)


        if positions is not None:
            return positions
        else:
            print("no positions returned by get_start_end_locations")
            return None

