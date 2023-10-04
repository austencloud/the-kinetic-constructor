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
    def __init__(self, staff_manager, graphboard_view, graphboard_scene, info_tracker, main_window, arrow_handler, exporter, context_menu_handler, grid, parent=None):
        self.staff_manager = staff_manager
        self.parent = parent
        self.graphboard_view = graphboard_view
        self.info_tracker = info_tracker
        self.graphboard_scene = graphboard_scene
        self.current_letter = None  # Add this line
        self.main_window = main_window
        self.arrow_handler = arrow_handler
        self.svg_handler = Svg_Handler()
        self.context_menu_handler = context_menu_handler
        self.exporter = exporter
        self.grid = grid

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

                # Check if the current combination has one 'anti' and one 'pro'
                motion_types = [arrow_dict['motion_type'] for arrow_dict in combination if 'motion_type' in arrow_dict]
                is_hybrid = motion_types.count('anti') == 1 and motion_types.count('pro') == 1


                # Iterate over the arrow dictionaries in the list
                for arrow_dict in combination:
                    print("iterating over arrow_dict in combination")
                    # Check if the dictionary has all the keys you need
                    if all(key in arrow_dict for key in ['color', 'motion_type', 'rotation_direction', 'quadrant']):
                        # Get the color and motion_type of the arrow
                        color = arrow_dict['color']
                        motion_type = arrow_dict['motion_type']

                        # Create the file name
                        file_name = f"{letter}_{start_position}_{end_position}"
                        if motion_type == 'pro' and is_hybrid and color == 'red':
                            file_name += f"_r-pro_l-anti"
                        elif motion_type == 'anti' and is_hybrid and color == 'red':
                            file_name += f"_r-anti_l-pro"
                        file_name += ".svg"


                        # Write the SVG to a file
                        output_file_path = os.path.join(self.output_dir, file_name)
                        self.exporter = Exporter(self.graphboard_view, self.graphboard_scene, self.staff_manager, self.grid)
                        print(output_file_path)
                        self.exporter.export_to_svg(output_file_path)

                
                # Clear the graphboard for the next combination
                self.graphboard_view.clear()

    def generate_pictograph(self, letter, staff_manager):
        #delete all items
        self.graphboard_view.clear()

        # Get the list of possible combinations for the letter
        combinations = self.letters.get(letter, [])
        if not combinations:
            print(f"No combinations found for letter {letter}")
            self.graphboard_view.update_letter(None)
            self.info_tracker.update()
            return

        self.current_letter = letter  # Store the current letter
        print(f"Generating {self.current_letter}")
        self.graphboard_view.update_letter(self.current_letter)
        # Choose a combination at random
        combination_set = random.choice(combinations)

        # Create a list to store the created arrows
        created_arrows = []

        # Find the optimal positions dictionary in combination_set
        optimal_positions = next((d for d in combination_set if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)

        for combination in combination_set:

            # Check if the dictionary has all the keys you need
            if all(key in combination for key in ['color', 'motion_type', 'rotation_direction', 'quadrant', 'turns']):
                if combination['motion_type'] == 'static':
                    svg_file = f"images/arrows/blank.svg"
                    arrow = Arrow(svg_file, self.graphboard_view, self.info_tracker, self.svg_handler, self.arrow_handler, combination['motion_type'], self.staff_manager)
                elif combination['motion_type'] == 'anti' or combination['motion_type'] == 'pro':
                    svg_file = f"images/arrows/shift/{combination['motion_type']}/{combination['color']}_{combination['motion_type']}_{combination['rotation_direction']}_{combination['quadrant']}_{combination['turns']}.svg"
                    arrow = Arrow(svg_file, self.graphboard_view, self.info_tracker, self.svg_handler, self.arrow_handler, combination['motion_type'], self.staff_manager)
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
                    # Calculate the position to center the arrow at the optimal position
                    pos = QPointF(optimal_position['x'], optimal_position['y']) - arrow.boundingRect().center()
                    arrow.setPos(pos)
                else:
                    if arrow.get_attributes()['quadrant'] != "None":
                        pos = self.graphboard_view.get_quadrant_center(arrow.get_attributes()['quadrant']) - arrow.boundingRect().center()
            else:
                # Calculate the position to center the arrow at the quadrant center
                pos = self.graphboard_view.get_quadrant_center(arrow.get_attributes()['quadrant']) - arrow.boundingRect().center()
                arrow.setPos(pos)

        self.staff_manager.update_graphboard_staffs(self.graphboard_scene)
        # created_arrows should be a list
        self.info_tracker.update()

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
