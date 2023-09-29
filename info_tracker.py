from arrow import Arrow
from handlers import Arrow_Handler
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
import json
import os
from data import positions_map
from staff import Staff
class Info_Tracker:
    arrowDeleted = pyqtSignal()  # New signal to indicate an arrow has been deleted

    
    def __init__(self, graphboard, label, main_window, staff_manager, arrow_handler):
        self.graphboard = graphboard
        self.label = label
        self.previous_state = None 
        self.main_window = main_window
        self.label.setFont(QFont('Helvetica', 14))
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        self.label.setAlignment(Qt.AlignTop)
        self.letters = self.load_letters()
        self.staff_manager = staff_manager
        self.is_initialized = False  # Add this flag to indicate initialization status
        # Inside your Info_Tracker class or wherever you're initializing Arrow_Handler
        self.arrow_handler = arrow_handler
        self.arrow_handler.arrowDeleted.connect(self.update)  # Assuming `update` is the method that updates the letter

    def set_initialized(self, status):
        self.is_initialized = status


    def start(self):
        self.previous_state = self.get_current_state()

    def set_graphboard(self, graphboard):
        self.graphboard = graphboard

    def get_current_state(self):
        state = {}
        arrow_count = 0  # Count the number of Arrow instances
        for item in self.graphboard.items():
            if isinstance(item, Arrow):
                arrow_count += 1
                # existing code for capturing the state
        
        if arrow_count == 0:
            return None  # No arrows on the board
        else:
            return state


    def get_current_letter(self):
        if self.letter is not None:
            return self.letter
        else:
            print("No self.letter found")
    
    def check_for_changes(self):
        current_state = self.get_current_state()
        if current_state != self.previous_state:
            self.update()
            self.previous_state = current_state
    
    def get_positional_relationship(self, start1, end1, start2, end2):
        start1_compass = Arrow.get_position_from_locations(start1, start1)
        end1_compass = Arrow.get_position_from_locations(end1, end1)
        start2_compass = Arrow.get_position_from_locations(start2, start2)
        end2_compass = Arrow.get_position_from_locations(end2, end2)

        if set(start1_compass) == set(start2_compass):
            start_location = "beta"
        elif set(start1_compass) == set(["n", "s"]) or set(start1_compass) == set(["e", "w"]):
            start_location = "alpha"
        else:
            start_location = "gamma"

        if set(end1_compass) == set(end2_compass):
            end_location = "beta"
        elif set(end1_compass) == set(["n", "s"]) or set(end1_compass) == set(["e", "w"]):
            end_location = "alpha"
        else:
            end_location = "gamma"

        return start_location + " to " + end_location
            
    def generate_arrow_positions():
        arrow_positions = {}
        from main import Main_Window
        for dirpath, dirnames, filenames in os.walk(Main_Window.ARROW_DIR):
            for filename in filenames:
                if filename.endswith('.svg'):
                    parts = filename.split('_')
                    arrow_type = parts[1]
                    rotation = parts[2]
                    quadrant = parts[3].split('.')[0]
                    if arrow_type == "anti":
                        if rotation == "l":
                            start_location, end_location = ("n", "s")
                        else:  # rotation == "r"
                            end_location, start_location = ("n", "s")
                    else:  # arrow_type == "iso"
                        if rotation == "l":
                            start_location, end_location = ("n", "s")
                        else:  # rotation == "r"
                            end_location, start_location = ("n", "s")
                    arrow_positions[filename] = (start_location, end_location)
        return arrow_positions
    
    def load_letters(self):
        try:
            with open('pictographs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        
    def update(self):
        print("update method called")
        if not self.is_initialized:
            return
        current_combination = []
        arrow_count = 0  # Count the number of Arrow instances
        staff_count = 0  # Count the number of Staff instances

        for item in self.graphboard.items():
            if isinstance(item, Arrow):
                arrow_count += 1
                attributes = item.get_attributes()
                current_combination.append(attributes)
            elif isinstance(item, Staff):  # Assuming Staff is the class name for staves
                staff_count += 1

        current_combination = sorted(current_combination, key=lambda x: x['color'])

        self.letters = self.load_letters()

        blue_text = "<h2 style='color: #0000FF'>Left</h2>Quadrant: <br>Rotation: <br>Type: <br>Start: <br>End: <br>"
        red_text = "<h2 style='color: #FF0000'>Right</h2>Quadrant: <br>Rotation: <br>Type: <br>Start: <br>End: <br>"
        letter_text = "<h2>Letter</h2>"

        if arrow_count >= 1 and staff_count >= 2:  # At least one arrow and two staves are needed
            for letter, combinations in self.letters.items():
                combinations = [sorted([x for x in combination if 'color' in x], key=lambda x: x['color']) for combination in combinations]
                if current_combination in combinations:
                    letter_text += f"<span style='font-size: 140px; font-weight: bold;'>{letter}</span>"
                    start_position, end_position = self.get_positions()
                    letter_text += f"<h4>{start_position} → {end_position}</h4>"
                    self.letter = letter
                    break
            else:
                self.letter = None
        else:
            self.letter = None

        self.graphboard.update_letter(self.letter)  # Update the letter on the graphboard

        # ... (rest of the code remains the same, including updating blue_text and red_text)
        self.label.setText("<table><tr><td width=300>" + blue_text + "</td></tr><tr><td width=300>" + red_text + "</td></tr></table>")
    
    def get_positions(self):
        positions = []
        arrow_items = []
        counter = 1
        start_location_red = None
        end_location_red = None
        start_location_blue = None
        end_location_blue = None
        color_red = None
        color_blue = None
        for item in self.graphboard.items():
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
            start_position = positions_map.get(start_key)
            end_position = positions_map.get(end_key)
            positions.append(start_position)
            positions.append(end_position)


        if positions is not None:
            return positions
        else:
            print("no positions returned by get_positions")
            return None

    def update_position_label(self, position_label):
        self.position_label = position_label
        start_position, end_position = self.get_positions()
        self.position_label.setText(f"Start: {start_position}\nEnd: {end_position}")

