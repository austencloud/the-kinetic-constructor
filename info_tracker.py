from arrow import Arrow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import json
import os
from data import positions_map

class Info_Tracker:
    def __init__(self, artboard, label, main_window, staff_manager):
        self.artboard = artboard
        self.label = label
        self.previous_state = None 
        self.main_window = main_window
        self.label.setFont(QFont('Helvetica', 14))
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        self.label.setAlignment(Qt.AlignTop)
        self.letterCombinations = self.load_letters()
        self.staff_manager = staff_manager  # Add this line

    def start(self):
        self.previous_state = self.get_current_state()

    def set_artboard(self, artboard):
        self.artboard = artboard

    def get_current_state(self):
        state = {}
        for item in self.artboard.items():
            if isinstance(item, Arrow):
                state[item] = item.get_attributes()
        return state

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
            with open('letterCombinations.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def update(self):
        current_combination = []

        for item in self.artboard.items():
            if isinstance(item, Arrow):
                attributes = item.get_attributes()
                current_combination.append(attributes)

        current_combination = sorted(current_combination, key=lambda x: x['color'])

        self.letterCombinations = self.load_letters()
        blue_text = "<h2>Left</h2>"
        red_text = "<h2>Right</h2>"
        letter_text = "<h2>Letter</h2>"

        for letter, combinations in self.letterCombinations.items():
            combinations = [sorted([x for x in combination if 'color' in x], key=lambda x: x['color']) for combination in combinations]  # Ignore the first dictionary which contains optimal positions
            if current_combination in combinations:
                letter_text += f"<h3 style='font-size: 50px'>{letter}</h3>"
                start_position, end_position = self.get_positions()
                letter_text += f"<h4>Start: {start_position}</h4>"
                letter_text += f"<h4>End: {end_position}</h4>"

        if hasattr(self.main_window, 'staff'):
            self.main_window.staff.update_position(self.arrow.end_location)

        for item in self.artboard.items():
            if isinstance(item, Arrow):
                attributes = item.get_attributes()
                current_combination.append(attributes)
                color = attributes.get('color', 'N/A')
                rotation = attributes.get('rotation', 'N/A')
                color_text = f"<font color='{color}'>Color: {color}</font>"
                if rotation == 'l':
                    rotation = 'Anti-clockwise'
                else: # rotation == 'r'
                    rotation = 'Clockwise'
                if color == 'blue':
                    blue_text += f"{color_text}<br>"
                    blue_text += f"Quadrant: {attributes.get('quadrant', 'N/A').upper()}<br>"
                    blue_text += f"Rotation: {rotation}<br>"
                    blue_text += f"Type: {attributes.get('type', 'N/A').capitalize()}<br>"
                    blue_text += f"Start: {attributes.get('start_location', 'N/A').capitalize()}<br>"
                    blue_text += f"End: {attributes.get('end_location', 'N/A').capitalize()}<br>"
                    blue_text += "<br>"
                elif color == 'red':
                    red_text += f"{color_text}<br>"
                    red_text += f"Quadrant: {attributes.get('quadrant', 'N/A').upper()}<br>"
                    red_text += f"Rotation: {rotation}<br>"
                    red_text += f"Type: {attributes.get('type', 'N/A').capitalize()}<br>"
                    red_text += f"Start: {attributes.get('start_location', 'N/A').capitalize()}<br>"
                    red_text += f"End: {attributes.get('end_location', 'N/A').capitalize()}<br>"
                    red_text += "<br>"

        self.label.setText("<table><tr><td width=300>" + blue_text + "</td><td width=300>" + red_text + "</td><td width=100>" + letter_text + "</td></tr></table>")

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
        for item in self.artboard.items():
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
            print(positions)

        if positions is not None:
            return positions
        else:
            print("no positions returned by get_positions")
            return None

    def update_position_label(self, position_label):
        self.position_label = position_label
        start_position, end_position = self.get_positions()
        self.position_label.setText(f"Start: {start_position}\nEnd: {end_position}")

