from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QGraphicsItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QFont
import json
import random
from arrow import Arrow


class Pictograph_Generator():
    def __init__(self, staff_manager, artboard, artboard_view, artboard_scene, info_tracker, handlers, parent=None):
        self.staff_manager = staff_manager
        self.parent = parent
        self.artboard = artboard
        self.artboard_view = artboard_view
        self.info_tracker = info_tracker
        self.handlers = handlers
        self.artboard_scene = artboard_scene
        self.current_letter = None  # Add this line


    def initLetterButtons(self):
        # Create a new layout for the Word Constructor's widgets
        letter_buttons_layout = QVBoxLayout()
        # Define the rows of letters
        letter_rows = [
            ['A', 'B', 'C'],
            ['D', 'E', 'F'],
            ['G', 'H', 'I'],
            ['J', 'K', 'L'],
            ['M', 'N', 'O'],
            ['P', 'Q', 'R'],
            ['S', 'T', 'U', 'V'],
        ]
        for row in letter_rows:
            row_layout = QHBoxLayout()
            row_layout.setAlignment(Qt.AlignTop)
            for letter in row:
                button = QPushButton(letter, self.parent)
                font = QFont()
                font.setPointSize(20)
                button.setFont(font)
                button.setFixedSize(80, 80)
                button.clicked.connect(lambda _, l=letter: self.generatePictograph(l, self.staff_manager))  # pass staff_manager here
                row_layout.addWidget(button)
            letter_buttons_layout.addLayout(row_layout)
        
        return letter_buttons_layout

    def generatePictograph(self, letter, staff_manager):
        #delete all items
        self.artboard.clear()

        # Reload the JSON file
        with open('letters.json', 'r') as file:
            self.letters = json.load(file)

        # Get the list of possible combinations for the letter
        combinations = self.letters.get(letter, [])
        if not combinations:
            print(f"No combinations found for letter {letter}")
            return

        self.current_letter = letter  # Store the current letter

        # Choose a combination at random
        combination_set = random.choice(combinations)

        # Create a list to store the created arrows
        created_arrows = []

        # Find the optimal positions dictionary in combination_set
        optimal_positions = next((d for d in combination_set if 'optimal_red_location' in d and 'optimal_blue_location' in d), None)
        print(f"Optimal positions: {optimal_positions}")

        for combination in combination_set:
            # Check if the dictionary has all the keys you need
            if all(key in combination for key in ['color', 'type', 'rotation', 'quadrant']):
                svg = f"images/arrows/{combination['color']}_{combination['type']}_{combination['rotation']}_{combination['quadrant']}.svg"
                arrow = Arrow(svg, self.artboard_view, self.info_tracker, self.handlers)
                arrow.attributesChanged.connect(lambda: self.update_staff(arrow, staff_manager))
                arrow.set_attributes(combination)
                arrow.setFlag(QGraphicsItem.ItemIsMovable, True)
                arrow.setFlag(QGraphicsItem.ItemIsSelectable, True)

                # Add the created arrow to the list
                created_arrows.append(arrow)

        # Add the arrows to the scene
        for arrow in created_arrows:
            self.artboard_scene.addItem(arrow)

        for arrow in created_arrows:
            if optimal_positions:
                optimal_position = optimal_positions.get(f"optimal_{arrow.get_attributes()['color']}_location")
                if optimal_position:
                    print(f"Setting position for {arrow.get_attributes()['color']} arrow to optimal position: {optimal_position}")
                    # Calculate the position to center the arrow at the optimal position
                    pos = QPointF(optimal_position['x'], optimal_position['y']) - arrow.boundingRect().center()
                    arrow.setPos(pos)
                else:
                    print(f"No optimal position found for {arrow.get_attributes()['color']} arrow. Setting position to quadrant center.")
                    # Calculate the position to center the arrow at the quadrant center
                    pos = self.artboard.getQuadrantCenter(arrow.get_attributes()['quadrant']) - arrow.boundingRect().center()
                    arrow.setPos(pos)
            else:
                print(f"No optimal positions dictionary found. Setting position for {arrow.get_attributes()['color']} arrow to quadrant center.")
                # Calculate the position to center the arrow at the quadrant center
                pos = self.artboard.getQuadrantCenter(arrow.get_attributes()['quadrant']) - arrow.boundingRect().center()
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
        self.artboard_view.arrowMoved.emit()
    
    def get_current_letter(self):
        return self.current_letter  # Add this method

    def update_staff(self, arrow, staff_manager):
        arrows = [arrow] if not isinstance(arrow, list) else arrow

        staff_positions = [arrow.end_location.upper() + '_staff_' + arrow.color for arrow in arrows]

        for element_id, staff in staff_manager.staffs.items():
            if element_id in staff_positions:
                staff.show()
            else:
                staff.hide()

        self.staff_manager.check_and_replace_staves()
