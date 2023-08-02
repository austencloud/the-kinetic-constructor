from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont
import json
import random
from arrow import Arrow
from handlers import Svg_Handler, Context_Menu_Handler

class Pictograph_Generator():
    def __init__(self, staff_manager, graphboard, graphboard_view, graphboard_scene, info_tracker, handlers, main_window, arrow_manipulator, parent=None):
        self.staff_manager = staff_manager
        self.parent = parent
        self.graphboard = graphboard
        self.graphboard_view = graphboard_view
        self.info_tracker = info_tracker
        self.handlers = handlers
        self.graphboard_scene = graphboard_scene
        self.current_letter = None  # Add this line
        self.main_window = main_window
        self.arrow_manipulator = arrow_manipulator
        self.svg_handler = Svg_Handler()
        self.context_menu_handler = Context_Menu_Handler(self.graphboard_scene)

    def generate_pictograph(self, letter, staff_manager):
        #delete all items
        self.graphboard.clear()

        # Reload the JSON file
        with open('pictographs.json', 'r') as file:
            self.letters = json.load(file)

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
                arrow = Arrow(svg_file, self.graphboard_view, self.info_tracker, self.svg_handler, self.arrow_manipulator)
                arrow.attributesChanged.connect(lambda: self.update_staff(arrow, staff_manager))
                arrow.attributesChanged.connect(lambda: self.update_arrow_position(arrow))  # Connect the signal to the slot
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
                    print(f"Setting position for {arrow.get_attributes()['color']} arrow to optimal position: {optimal_position}")
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

        for combination in combination_set:
            if all(key in combination for key in ['start_position', 'end_position']):
                #print the start/end position values
                start_position = combination['start_position']
                end_position = combination['end_position']

        # self.info_tracker.update_position_label(self.position_label)  # Remove this line
        self.staff_manager.remove_non_beta_staves()
        # Update the info label
        self.info_tracker.update()
        self.graphboard_view.arrowMoved.emit()
    
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
