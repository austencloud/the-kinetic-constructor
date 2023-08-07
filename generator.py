from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont
import json
import random
import os
from arrow import Arrow
from handlers import Svg_Handler
from lxml import etree
from menus import Context_Menu_Handler
from exporter import Exporter
class Pictograph_Generator():
    def __init__(self, staff_manager, graphboard, graphboard_scene, info_tracker, main_window, arrow_handler, exporter, context_menu_handler, grid, ui_setup, parent=None):
        self.staff_manager = staff_manager
        self.parent = parent
        self.graphboard = graphboard
        self.info_tracker = info_tracker
        self.graphboard_scene = graphboard_scene
        self.current_letter = None  # Add this line
        self.main_window = main_window
        self.arrow_handler = arrow_handler
        self.svg_handler = Svg_Handler()
        self.context_menu_handler = context_menu_handler
        self.exporter = exporter
        self.grid = grid
        self.ui_setup = ui_setup
        # Load the JSON file
        with open('pictographs.json', 'r') as file:
            self.letters = json.load(file)
        self.output_dir = "images\\pictographs\\"

    def generate_all_pictographs(self, staff_manager):
        # Create the output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

        # Iterate over all combinations for each letter
        for letter, combinations in self.letters.items():
            for combination in combinations:
                # Generate the pictograph for the combination
                self.generate_pictograph(letter, staff_manager)

                # Find the dictionary in the combination list that contains the 'start_position' and 'end_position' keys
                positions_dict = next((d for d in combination if 'start_position' in d and 'end_position' in d), None)
                if positions_dict is None:
                    continue

                # Get the start and end positions
                start_position = positions_dict['start_position'].replace('alpha', 'a').replace('beta', 'b').replace('gamma', 'g')
                end_position = positions_dict['end_position'].replace('alpha', 'a').replace('beta', 'b').replace('gamma', 'g')

                # Check if the current combination has one 'anti' and one 'iso'
                types = [arrow_dict['type'] for arrow_dict in combination if 'type' in arrow_dict]
                is_hybrid = types.count('anti') == 1 and types.count('iso') == 1

                # print(combination)

                # Iterate over the arrow dictionaries in the list
                for arrow_dict in combination:
                    print("iterating over arrow_dict in combination")
                    # Check if the dictionary has all the keys you need
                    if all(key in arrow_dict for key in ['color', 'type', 'rotation', 'quadrant']):
                        # Get the color and type of the arrow
                        color = arrow_dict['color']
                        type = arrow_dict['type']

                        # Create the file name
                        file_name = f"{letter}_{start_position}_{end_position}"
                        if type == 'iso' and is_hybrid and color == 'red':
                            file_name += f"_r-iso_l-anti"
                        elif type == 'anti' and is_hybrid and color == 'red':
                            file_name += f"_r-anti_l-iso"
                        file_name += ".svg"


                        # Write the SVG to a file
                        output_file_path = os.path.join(self.output_dir, file_name)
                        self.exporter = Exporter(self.graphboard, self.graphboard_scene, self.staff_manager, self.grid)
                        print(output_file_path)
                        self.exporter.export_to_svg(output_file_path)

                
                # Clear the graphboard for the next combination
                self.graphboard.clear()





    def generate_pictograph(self, letter, staff_manager):
        #delete all items
        self.graphboard.clear()

        # Get the list of possible combinations for the letter
        combinations = self.letters.get(letter, [])
        if not combinations:
            print(f"No combinations found for letter {letter}")
            return

        self.current_letter = letter  # Store the current letter
        print(f"Generating {self.current_letter}")
        # Choose a combination at random
        combination_set = random.choice(combinations)

        # Create a list to store the created arrows
        created_arrows = []

        # Find the optimal positions dictionary in combination_set
        optimal_positions = next((d for d in combination_set if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)


        for combination in combination_set:
            # Check if the dictionary has all the keys you need
            if all(key in combination for key in ['color', 'type', 'rotation', 'quadrant']):
                svg_file = f"images/arrows/{combination['color']}_{combination['type']}_{combination['rotation']}_{combination['quadrant']}.svg"
                arrow = Arrow(svg_file, self.graphboard, self.info_tracker, self.svg_handler, self.arrow_handler, self.ui_setup)
                arrow.attributesChanged.connect(lambda: self.update_staff(arrow, staff_manager))
                arrow.set_attributes(combination)
                arrow.setFlag(QGraphicsItem.ItemIsMovable, True)
                arrow.setFlag(QGraphicsItem.ItemIsSelectable, True)

                # Add the created arrow to the list
                created_arrows.append(arrow)

        # Add the arrows to the scene
        for arrow in created_arrows:
            self.graphboard_scene.addItem(arrow)

        for arrow in created_arrows:
            if optimal_positions:
                optimal_position = optimal_positions.get(f"optimal_{arrow.get_attributes()['color']}_location")
                if optimal_position:
                    # print(f"Setting position for {arrow.get_attributes()['color']} arrow to optimal position: {optimal_position}")
                    # Calculate the position to center the arrow at the optimal position
                    pos = QPointF(optimal_position['x'], optimal_position['y']) - arrow.boundingRect().center()
                    arrow.setPos(pos)
                else:
                    # Calculate the position to center the arrow at the quadrant center
                    pos = self.graphboard.get_quadrant_center(arrow.get_attributes()['quadrant']) - arrow.boundingRect().center()
                    arrow.setPos(pos)
            else:
                # Calculate the position to center the arrow at the quadrant center
                pos = self.graphboard.get_quadrant_center(arrow.get_attributes()['quadrant']) - arrow.boundingRect().center()
                arrow.setPos(pos)

                # Call the update_staff function for the arrow
                self.update_staff(arrow, staff_manager)

        # Update the info label
        self.info_tracker.update()
        self.graphboard.arrowMoved.emit()
    
    def get_current_letter(self):
        return self.current_letter

    def update_staff(self, arrow, staff_manager):
        arrows = [arrow] if not isinstance(arrow, list) else arrow

        staff_positions = [arrow.end_location.upper() + '_staff_' + arrow.color for arrow in arrows]

        for element_id, staff in staff_manager.graphboard_staffs.items():
            if element_id in staff_positions:
                staff.show()
            else:
                staff.hide()

        self.staff_manager.check_and_replace_staves()
