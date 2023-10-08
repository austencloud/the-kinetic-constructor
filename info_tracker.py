from objects.arrow import Arrow
from objects.staff import Staff
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import json
import os
from data import positions_map, letter_types

class Info_Tracker:
    def __init__(self, graphboard_view, label, staff_manager, json_manager):
        self.remaining_staff = {}
        self.previous_state = None 
        self.graphboard_view = graphboard_view
        self.staff_manager = staff_manager
        self.label = label
        self.json_manager = json_manager
        self.letters = self.json_manager.load_all_letters()    

        if self.label:
            self.label.setFont(QFont('Helvetica', 14))
            self.label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
            self.label.setAlignment(Qt.AlignTop)



    def connect_graphboard_view(self, graphboard_view):
        self.graphboard_view = graphboard_view

    ### GETTERS ###

    def get_current_letter(self):
        if self.letter is not None:
            return self.letter
        else:
            print("No self.letter found")
    
    def check_for_changes(self):
        current_state = {}
        for item in self.graphboard_view.items():
            if isinstance(item, Arrow):
                current_state[item] = item.get_attributes()
        if current_state != self.previous_state:
            self.update()
            self.previous_state = current_state

    def check_for_remaining_staff(self, color):
        for item in self.graphboard_view.items():
            if isinstance(item, Staff) and item.color == color:  # Assuming you have a Staff class
                return item
        return None

    def determine_current_letter_and_type(self):
        current_combination = []
        for item in self.graphboard_view.items():
            if isinstance(item, Arrow):
                attributes = item.get_attributes()
                sorted_attributes = {k: attributes[k] for k in sorted(attributes.keys())}
                current_combination.append(sorted_attributes)
        # Sort the list of dictionaries by the 'color' key
        current_combination = sorted(current_combination, key=lambda x: x['color'])
        letter_type = None
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

        return self.letter, letter_type  # Always return two values



    def generate_arrow_positions():
        arrow_positions = {}
        from main import Main_Window
        for dirpath, dirnames, filenames in os.walk(Main_Window.ARROW_DIR):
            for filename in filenames:
                if filename.endswith('.svg'):
                    parts = filename.split('_')
                    motion_type = parts[1]
                    rotation_direction = parts[2]
                    quadrant = parts[3].split('.')[0]
                    if motion_type == "anti":
                        if rotation_direction == "l":
                            start_location, end_location = ("n", "s")
                        else:  # rotation_direction == "r"
                            end_location, start_location = ("n", "s")
                    else:  # motion_type == "pro"
                        if rotation_direction == "l":
                            start_location, end_location = ("n", "s")
                        else:  # rotation_direction == "r"
                            end_location, start_location = ("n", "s")
                    arrow_positions[filename] = (start_location, end_location)
        return arrow_positions
    
   
    def update_from_arrow_manager(self, remaining_staff):
        self.remaining_staff = remaining_staff
        self.update()  # Assuming update() refreshes the display    
    
    def update(self):
        current_combination = []
        self.remaining_staff = {}  # Initialize an empty dictionary to store remaining staff info

        for item in self.graphboard_view.items():
            if isinstance(item, Arrow):
                attributes = item.get_attributes()
                current_combination.append(attributes)

        current_combination = sorted(current_combination, key=lambda x: x['color'])
        self.letters = self.json_manager.load_all_letters()


        blue_text = "<h2 style='color: #0000FF'>Left</h2>Quadrant: <br>Rotation: <br>Type: <br>Start: <br>End: <br>Turns: <br>"
        red_text = "<h2 style='color: #FF0000'>Right</h2>Quadrant: <br>Rotation: <br>Type: <br>Start: <br>End: <br>Turns: <br>"
        letter_text = ""

        no_blue_arrows = True
        no_red_arrows = True

        for item in self.graphboard_view.items():
            if isinstance(item, Arrow):
                attributes = item.get_attributes()
                color = attributes.get('color', 'N/A')
                if not item.isVisible():
                    attributes['motion_type'] = 'static'

                if attributes['motion_type'] == 'pro' or attributes['motion_type'] == 'anti':
                    if color == 'blue':
                        no_blue_arrows = False
                        blue_text = blue_text.replace("Quadrant: ", f"Quadrant: {attributes.get('quadrant').upper()}")
                        blue_text = blue_text.replace("Rotation: ", f"Rotation: {item.rotation_direction.capitalize()}")
                        blue_text = blue_text.replace("Type: ", f"Type: {attributes.get('motion_type', 'N/A').capitalize()}")
                        blue_text = blue_text.replace("Start: ", f"Start: {attributes.get('start_location', 'N/A').capitalize()}")
                        blue_text = blue_text.replace("End: ", f"End: {attributes.get('end_location', 'N/A').capitalize()}")
                        blue_text = blue_text.replace("Turns: ", f"Turns: {attributes.get('turns', 'N/A')}")
                    elif color == 'red':
                        no_red_arrows = False
                        red_text = red_text.replace("Quadrant: ", f"Quadrant: {attributes.get('quadrant').upper()}")
                        red_text = red_text.replace("Rotation: ", f"Rotation: {attributes.get('rotation_direction').capitalize()}")
                        red_text = red_text.replace("Type: ", f"Type: {attributes.get('motion_type', 'N/A').capitalize()}")
                        red_text = red_text.replace("Start: ", f"Start: {attributes.get('start_location', 'N/A').capitalize()}")
                        red_text = red_text.replace("End: ", f"End: {attributes.get('end_location', 'N/A').capitalize()}")
                        red_text = red_text.replace("Turns: ", f"Turns: {attributes.get('turns', 'N/A')}")
                elif attributes['motion_type'] == 'static':
                    if color == 'blue':
                        no_blue_arrows = False
                        blue_text = blue_text.replace("Quadrant: ", f"Quadrant: {attributes.get('quadrant')}")
                        blue_text = blue_text.replace("Rotation: ", f"Rotation: {item.rotation_direction}")
                        blue_text = blue_text.replace("Type: ", f"Type: {attributes.get('motion_type', 'N/A').capitalize()}")
                        blue_text = blue_text.replace("Start: ", f"Start: {attributes.get('start_location', 'N/A').capitalize()}")
                        blue_text = blue_text.replace("End: ", f"End: {attributes.get('end_location', 'N/A').capitalize()}")
                        blue_text = blue_text.replace("Turns: ", f"Turns: {attributes.get('turns', 'N/A')}")
                    elif color == 'red':
                        no_red_arrows = False
                        red_text = red_text.replace("Quadrant: ", f"Quadrant: {attributes.get('quadrant')}")
                        red_text = red_text.replace("Rotation: ", f"Rotation: {attributes.get('rotation_direction')}")
                        red_text = red_text.replace("Type: ", f"Type: {attributes.get('motion_type', 'N/A').capitalize()}")
                        red_text = red_text.replace("Start: ", f"Start: {attributes.get('start_location', 'N/A').capitalize()}")
                        red_text = red_text.replace("End: ", f"End: {attributes.get('end_location', 'N/A').capitalize()}")
                        red_text = red_text.replace("Turns: ", f"Turns: {attributes.get('turns', 'N/A')}")

        # Determine the current letter and its type
        self.letter, current_letter_type = self.determine_current_letter_and_type()
        
        # Update the letter_text based on the type, not the letter itself
        letter_text = ""
        
        for letter, combinations in self.letters.items():
            combinations = [sorted([x for x in combination if 'color' in x], key=lambda x: x['color']) for combination in combinations]  # Ignore the first dictionary which contains optimal positions
        
            if current_combination in combinations:
                    letter_text += f"<span style='font-size: 40px; font-weight: bold;'>{current_letter_type}</span>"
                    start_position, end_position = self.get_positions()
                    letter_text += f"<h4>{start_position} → {end_position}</h4>"
                    self.letter = letter 
                    break  
                
        else:  # This will execute if the for loop completes without a 'break'
            self.letter = None
            self.graphboard_view.update_letter(None)   


        if self.letter is not None:
            self.graphboard_view.update_letter(self.letter)

        self.label.setText("<table><tr><td width=300>" + blue_text + "</td></tr><tr><td width=300>" + red_text + "</td></tr><tr><td width=100>" + letter_text + "</td></tr></table>")

        # Initialize an empty dictionary to store remaining staff info
        self.remaining_staff = {}

               
        if no_blue_arrows and 'blue' in self.remaining_staff:
            blue_text = blue_text.replace("Quadrant: ", f"Quadrant: {self.remaining_staff['blue']['quadrant'].upper()}")
            blue_text = blue_text.replace("Rotation: ", f"Rotation: {self.remaining_staff['blue']['rotation'].upper()}")
            blue_text = blue_text.replace("Motion: ", f"Motion: {self.remaining_staff['blue']['motion_type'].upper()}")
            blue_text = blue_text.replace("Start: ", f"Start: {self.remaining_staff['blue']['start'].upper()}")
            blue_text = blue_text.replace("End: ", f"End: {self.remaining_staff['blue']['end'].upper()}")
            blue_text = blue_text.replace("Turns: ", f"Turns: {self.remaining_staff['blue']['turns']}")

        if no_red_arrows and 'red' in self.remaining_staff:
            red_text = red_text.replace("Quadrant: ", f"Quadrant: {self.remaining_staff['red']['quadrant'].upper()}")
            red_text = red_text.replace("Rotation: ", f"Rotation: {self.remaining_staff['red']['rotation'].upper()}")
            red_text = red_text.replace("Motion: ", f"Motion: {self.remaining_staff['red']['motion_type'].upper()}")
            red_text = red_text.replace("Start: ", f"Start: {self.remaining_staff['red']['start'].upper()}")
            red_text = red_text.replace("End: ", f"End: {self.remaining_staff['red']['end'].upper()}")
            red_text = red_text.replace("Turns: ", f"Turns: {self.remaining_staff['red']['turns']}")

        self.staff_manager.update_graphboard_staffs(self.graphboard_view.scene())

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

