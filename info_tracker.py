from arrow import Arrow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import json
import os
from data import positions_map, letter_types

class Info_Tracker:
    
    def __init__(self, graphboard, label, main_window, staff_manager):
        self.graphboard = graphboard
        self.label = label
        self.previous_state = None 
        self.main_window = main_window
        self.label.setFont(QFont('Helvetica', 14))
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        self.label.setAlignment(Qt.AlignTop)
        self.letters = self.load_letters()
        self.staff_manager = staff_manager


    def start(self):
        self.previous_state = self.get_current_state()

    def set_graphboard(self, graphboard):
        self.graphboard = graphboard

    def get_current_state(self):
        state = {}
        for item in self.graphboard.items():
            if isinstance(item, Arrow):
                state[item] = item.get_attributes()
        return state

    def get_current_letter(self):
        if self.letter is not None:
            return self.letter
        else:
            print("No self.letter found")
    
    def check_for_changes(self):
        current_state = self.get_current_state()
        print(f"Previous State: {self.previous_state}, Current State: {self.get_current_state}")

        if current_state != self.previous_state:
            self.update()
            self.previous_state = current_state

    def determine_current_letter(self):
        current_combination = []
        for item in self.graphboard.items():
            if isinstance(item, Arrow):
                attributes = item.get_attributes()
                sorted_attributes = {k: attributes[k] for k in sorted(attributes.keys())}
                current_combination.append(sorted_attributes)
        current_combination = sorted(current_combination, key=lambda x: x['color'])
        
        current_type = None  # Initialize current_type to None
        
        for letter, combinations in self.letters.items():
            combinations = [sorted([x for x in combination if 'color' in x], key=lambda x: x['color']) for combination in combinations]
            if current_combination in combinations:
                self.letter = letter
                for type, letters in letter_types.items():  # Determine the type if a letter is found
                    if self.letter in letters:
                        current_type = type
                        break
                return self.letter, current_type  # Return both values here
        
        self.letter = None  # Set to None if no match is found

        return self.letter, current_type  # Always return two values

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
                    rotation_direction = parts[2]
                    quadrant = parts[3].split('.')[0]
                    if arrow_type == "anti":
                        if rotation_direction == "l":
                            start_location, end_location = ("n", "s")
                        else:  # rotation_direction == "r"
                            end_location, start_location = ("n", "s")
                    else:  # arrow_type == "pro"
                        if rotation_direction == "l":
                            start_location, end_location = ("n", "s")
                        else:  # rotation_direction == "r"
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
        current_combination = []

        for item in self.graphboard.items():
            if isinstance(item, Arrow):
                attributes = item.get_attributes()
                current_combination.append(attributes)

        current_combination = sorted(current_combination, key=lambda x: x['color'])
        print(f"All combinations: {self.letters}")

        print(f"current_combination: {current_combination}")
        self.letters = self.load_letters()
        
        # Determine the current letter and its type
        self.letter, current_type = self.determine_current_letter()
        
        # Update the letter_text based on the type, not the letter itself
        letter_text = "<h2>Type</h2>"
        
        if current_type is not None:
            letter_text += f"<span style='font-size: 140px; font-weight: bold;'>{current_type}</span>"
        else:
            letter_text += "<span style='font-size: 140px; font-weight: bold;'>Unknown</span>"
        

        blue_text = "<h2 style='color: #0000FF'>Left</h2>Quadrant: <br>Rotation: <br>Type: <br>Start: <br>End: <br>Turns: <br>"
        red_text = "<h2 style='color: #FF0000'>Right</h2>Quadrant: <br>Rotation: <br>Type: <br>Start: <br>End: <br>Turns: <br>"
        letter_text = ""

        for letter, combinations in self.letters.items():
            combinations = [sorted([x for x in combination if 'color' in x], key=lambda x: x['color']) for combination in combinations]  # Ignore the first dictionary which contains optimal positions
            
            if current_combination in combinations:
                letter_text += f"<span style='font-size: 40px; font-weight: bold;'>{current_type}</span>"
                start_position, end_position = self.get_positions()
                letter_text += f"<h4>{start_position} → {end_position}</h4>"
                self.letter = letter 
                break  
        else:  # This will execute if the for loop completes without a 'break'
            print("No letter found")
            self.letter = None
            self.graphboard.update_letter(None)   


        if hasattr(self.main_window, 'staff'):
            self.main_window.staff.update_position(self.arrow.end_location)

        for item in self.graphboard.items():
            if isinstance(item, Arrow):
                attributes = item.get_attributes()
                current_combination.append(attributes)
                color = attributes.get('color', 'N/A')
                rotation_direction = attributes.get('rotation_direction', 'N/A')
                end_location = attributes.get('end_location', 'N/A')
                if end_location is None:
                    break
                if rotation_direction == 'l':
                    rotation_direction = 'Anti-clockwise'
                else: # rotation_direction == 'r'
                    rotation_direction = 'Clockwise'
                if color == 'blue':
                    blue_text = blue_text.replace("Quadrant: ", f"Quadrant: {attributes.get('quadrant').upper()}")
                    blue_text = blue_text.replace("Rotation: ", f"Rotation: {rotation_direction}")
                    blue_text = blue_text.replace("Type: ", f"Type: {attributes.get('type', 'N/A').capitalize()}")
                    blue_text = blue_text.replace("Start: ", f"Start: {attributes.get('start_location', 'N/A').capitalize()}")
                    blue_text = blue_text.replace("End: ", f"End: {attributes.get('end_location', 'N/A').capitalize()}")
                    blue_text = blue_text.replace("Turns: ", f"Turns: {attributes.get('turns', 'N/A')}")
                elif color == 'red':
                    red_text = red_text.replace("Quadrant: ", f"Quadrant: {attributes.get('quadrant').upper()}")
                    red_text = red_text.replace("Rotation: ", f"Rotation: {rotation_direction}")
                    red_text = red_text.replace("Type: ", f"Type: {attributes.get('type', 'N/A').capitalize()}")
                    red_text = red_text.replace("Start: ", f"Start: {attributes.get('start_location', 'N/A').capitalize()}")
                    red_text = red_text.replace("End: ", f"End: {attributes.get('end_location', 'N/A').capitalize()}")
                    red_text = red_text.replace("Turns: ", f"Turns: {attributes.get('turns', 'N/A')}")

        if self.letter is not None:
            self.graphboard.update_letter(letter)
        self.label.setText("<table><tr><td width=300>" + blue_text + "</td></tr><tr><td width=300>" + red_text + "</td></tr><tr><td width=100>" + letter_text + "</td></tr></table>")

        
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

