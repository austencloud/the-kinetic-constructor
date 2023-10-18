from objects.arrow import Arrow
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from data.positions_map import positions_map
from data.letter_types import letter_types
from settings import GRAPHBOARD_SCALE
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
            font = QFont('Helvetica', int(16 * GRAPHBOARD_SCALE))
            self.label.setFont(font)
            self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)
            self.label.setAlignment(Qt.AlignmentFlag.AlignTop)

    def connect_graphboard_view(self, graphboard_view):
        self.graphboard_view = graphboard_view

    ### GETTERS ###

    def get_current_letter(self):
        self.letter = self.determine_current_letter_and_type()[0]
        if self.letter is not None:
            return self.letter
    
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

        for arrow in [item for item in self.graphboard_view.items() if isinstance(item, Arrow)]:
            arrow.set_attributes_from_filename()

            if arrow.color == 'blue':
                no_blue_arrows = False
                blue_text = blue_text.replace("Quadrant: ", f"Quadrant: {arrow.quadrant.upper()}")
                blue_text = blue_text.replace("Rotation: ", f"Rotation: {arrow.rotation_direction.capitalize()}")
                blue_text = blue_text.replace("Type: ", f"Type: {arrow.motion_type.capitalize()}")
                blue_text = blue_text.replace("Start: ", f"Start: {arrow.start_location.capitalize()}")
                blue_text = blue_text.replace("End: ", f"End: {arrow.end_location.capitalize()}")
                blue_text = blue_text.replace("Turns: ", f"Turns: {arrow.turns}")
            elif arrow.color == 'red':
                no_red_arrows = False
                red_text = red_text.replace("Quadrant: ", f"Quadrant: {arrow.quadrant.upper()}")
                red_text = red_text.replace("Rotation: ", f"Rotation: {arrow.rotation_direction.capitalize()}")
                red_text = red_text.replace("Type: ", f"Type: {arrow.motion_type.capitalize()}")
                red_text = red_text.replace("Start: ", f"Start: {arrow.start_location.capitalize()}")
                red_text = red_text.replace("End: ", f"End: {arrow.end_location.capitalize()}")
                red_text = red_text.replace("Turns: ", f"Turns: {arrow.turns}")

        # Determine the current letter and its type
        self.letter, current_letter_type = self.determine_current_letter_and_type()
        
        # Update the letter_text based on the type, not the letter itself
        letter_text = ""
        
        for letter, combinations in self.letters.items():
            combinations = [sorted([x for x in combination if 'color' in x], key=lambda x: x['color']) for combination in combinations]  # Ignore the first dictionary which contains optimal positions
        
            if current_combination in combinations:
                    letter_text += f"<span style='font-size: 40px; font-weight: bold;'>{current_letter_type}</span>"
                    start_location, end_location = self.get_start_end_locations()
                    letter_text += f"<h4>{start_location} → {end_location}</h4>"
                    self.letter = letter 
                    break
                
        else:  # Letter isn't in the combinations
            self.letter = None
            self.graphboard_view.update_letter(None)   

        if self.letter is not None:
            self.graphboard_view.update_letter(self.letter)

        self.label.setText("<table><tr><td width=300>" + blue_text + "</td></tr><tr><td width=300>" + red_text + "</td></tr><tr><td width=100>" + letter_text + "</td></tr></table>")
        self.staff_manager.update_graphboard_staffs(self.graphboard_view.scene())

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

