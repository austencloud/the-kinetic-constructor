import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QScrollArea, QVBoxLayout, QGraphicsScene, QGraphicsView, QPushButton, QGraphicsItem, QLabel, QFileDialog, QCheckBox, QLineEdit, QFrame
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QTransform, QFont
from arrow import Arrow
from artboard import Artboard
from handlers import Handlers
from grid import Grid
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtSvg import QSvgRenderer
from staff import StaffManager
from data import *
import json
import random
from info_tracker import Info_Tracker
from sequence import SequenceConstructor
from pictograph import Pictograph
class Main_Window(QWidget):
    ARROW_DIR = 'images\\arrows'
    SVG_POS_Y = 250

    def __init__(self):
        super().__init__() 
        self.arrows = []
        svgs_full_paths = []
        self.scene = QGraphicsScene()
        self.grid = Grid('images\\grid\\grid.svg')

        self.info_label = QLabel(self)
        self.staff_manager = StaffManager(self.scene)
        self.infoTracker = Info_Tracker(None, self.info_label, self, self.staff_manager)
        self.artboard = Artboard(self.scene, self.grid, self.infoTracker, self.staff_manager)


        self.position_label = QLabel(self)
        font = QFont()
        font.setPointSize(20)
        self.position_label.setFont(font)
        self.position_label.setStyleSheet("font-family: Helvetica")
        self.position_label.move(10, 10)

        self.initUI()
        self.artboard.arrowMoved.connect(lambda: self.update_position_label)
        self.staff_manager.positionChanged.connect(self.update_position_label)

        self.letterCombinations = self.loadLetters()
        self.grid_renderer = QSvgRenderer('images\\grid\\grid.svg')

        for dirpath, dirnames, filenames in os.walk(self.ARROW_DIR):
            svgs_full_paths.extend([os.path.join(dirpath, filename) for filename in filenames if filename.endswith('.svg')])

        transform = QTransform()
        self.grid_center = QPointF(self.artboard.frameSize().width() / 2, self.artboard.frameSize().height() / 2)
        grid_size = 650
        transform.translate(self.grid_center.x() - (grid_size / 2), self.grid_center.y() - (grid_size / 2))
        self.grid.setTransform(transform)

    def initUI(self):
        self.setWindowTitle('Sequence Constructor')

        # initialize all layouts
        main_layout = QHBoxLayout()
        right_layout = QVBoxLayout()
        left_layout = QHBoxLayout()
        upper_right_laybout = QHBoxLayout()
        lower_right_layout = QHBoxLayout()
        artboard_layout = QVBoxLayout()
        button_layout = QVBoxLayout()
        info_layout = QVBoxLayout()
        upper_right_laybout.addLayout(button_layout)
        upper_right_laybout.addLayout(artboard_layout)
        upper_right_laybout.addLayout(info_layout)
        right_layout.addLayout(upper_right_laybout)
        right_layout.addLayout(lower_right_layout)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        # set the letter buttons
        letter_buttons_layout = self.initLetterButtons(self.staff_manager)
        left_layout.addLayout(letter_buttons_layout)

        # set the artboard
        self.artboard_view = self.initArtboard() 
        self.infoTracker.set_artboard(self.artboard)
        artboard_layout.addWidget(self.artboard_view)

        #set up the arrowbox
        arrowbox = self.initArrowBox()
        left_layout.addWidget(arrowbox)
        left_layout.setAlignment(arrowbox, Qt.AlignTop)

        # set the buttons and info tracker
        buttons = self.initButtons() 
        button_layout.addLayout(buttons)
        info_layout.addWidget(self.info_label)
        upper_right_laybout.addLayout(button_layout)
        upper_right_laybout.addLayout(info_layout) 
        self.scene.changed.connect(self.infoTracker.update)
        
        self.initSequenceConstructor(lower_right_layout)

        ### Un-comment this code to enable the assign letter funtion ###
        # self.letterInput = QLineEdit(self)
        # right_layout.addWidget(self.letterInput)
        # self.assignLetterButton = QPushButton("Assign Letter", self)
        # self.assignLetterButton.clicked.connect(self.assignLetter)
        # right_layout.addWidget(self)

        right_layout.addWidget(self.position_label)
        self.setMinimumSize(2800, 1800)
        self.show()

    def initSequenceConstructor(self, layout):
        self.sequence_constructor = SequenceConstructor()
        self.sequence_container = QGraphicsView(self.sequence_constructor)
        
        #set the width and height
        self.sequence_container.setFixedSize(1500, 375)
        self.sequence_container.show()
        layout.addWidget(self.sequence_container)

    def initArrowBox(self):
        arrow_box = QScrollArea(self)
        arrowbox_scene = QGraphicsScene()
        for arrow in self.arrows:
            arrowbox_scene.addItem(arrow)  # use arrowbox_scene here
            arrow.attributesChanged.connect(self.infoTracker.update)
            arrow.attributesChanged.connect(lambda: self.update_staff(arrow, self.staff_manager))


        svgs_full_paths = []
        default_arrows = ['red_anti_r_ne.svg', 'red_iso_r_ne.svg', 'blue_anti_r_sw.svg', 'blue_iso_r_sw.svg']
        svg_item_count = 0

        for dirpath, dirnames, filenames in os.walk(self.ARROW_DIR):
            svgs_full_paths.extend([os.path.join(dirpath, filename) for filename in filenames if filename.endswith('.svg')])

        for i, svg in enumerate(svgs_full_paths):
            file_name = os.path.basename(svg)
            if file_name in default_arrows:
                self.handlers = Handlers(self.artboard, self.artboard_view, self.grid, self.artboard, self.infoTracker, self)
                self.artboard.set_handlers(self.handlers)
                arrow_item = Arrow(svg, self.artboard_view, self.infoTracker, self.handlers)
                arrow_item.setFlag(QGraphicsItem.ItemIsMovable, True)
                arrow_item.setFlag(QGraphicsItem.ItemIsSelectable, True)
                arrow_item.setScale(1)
                arrow_item.setPos(0, svg_item_count * self.SVG_POS_Y)
                arrowbox_scene.addItem(arrow_item) 
                arrow_item.attributesChanged.connect(self.infoTracker.update)

                svg_item_count += 1
                self.arrows.append(arrow_item)

        view = QGraphicsView(arrowbox_scene)
        view.setFrameShape(QFrame.NoFrame)
        arrow_box.setWidget(view)
        arrow_box.setWidgetResizable(True)
        arrow_box.setFixedSize(500, 1400)

        return arrow_box

    def initArtboard(self):
        grid_size = 650
        self.artboard.setFixedSize(750, 750)

        transform = QTransform()
        self.grid_center = QPointF(self.artboard.frameSize().width() / 2, self.artboard.frameSize().height() / 2)

        transform.translate(self.grid_center.x() - (grid_size / 2), self.grid_center.y() - (grid_size / 2))
        self.grid.setTransform(transform)

        self.artboard.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.artboard.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene.addItem(self.grid)



        return self.artboard

    def initButtons(self):
        self.handlers = Handlers(self.artboard, self.artboard_view, self.grid, self.artboard, self.infoTracker, self)
        self.artboard.set_handlers(self.handlers)
        masterbtnlayout = QVBoxLayout()
        buttonlayout = QHBoxLayout()
        buttonstack = QVBoxLayout()
        buttonstack.setAlignment(Qt.AlignTop)
        masterbtnlayout.setAlignment(Qt.AlignTop)
        buttonlayout.addLayout(buttonstack)
        masterbtnlayout.addLayout(buttonlayout)

        self.updatePositionButton = QPushButton("Update Position")
        self.updatePositionButton.clicked.connect(lambda: self.handlers.updatePositionInJson(*self.artboard.getCurrentArrowPositions()))
        buttonstack.addWidget(self.updatePositionButton)

        self.selectAllButton = QPushButton("Select All")
        self.selectAllButton.clicked.connect(self.handlers.selectAll)
        buttonstack.addWidget(self.selectAllButton)

        add_to_sequence_button = QPushButton("Add to Sequence")
        add_to_sequence_button.clicked.connect(lambda _: self.add_to_sequence(self.artboard, self.sequence_constructor))
        buttonstack.addWidget(add_to_sequence_button)

        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.handlers.deleteArrow)
        buttonstack.addWidget(self.deleteButton)

        self.rotateRightButton = QPushButton("Rotate Right")
        self.rotateRightButton.clicked.connect(lambda: self.handlers.rotateArrow("right"))
        buttonstack.addWidget(self.rotateRightButton)

        self.rotateLeftButton = QPushButton("Rotate Left")
        self.rotateLeftButton.clicked.connect(lambda: self.handlers.rotateArrow("left"))
        buttonstack.addWidget(self.rotateLeftButton)

        self.mirrorButton = QPushButton("Mirror")
        self.mirrorButton.clicked.connect(lambda: self.handlers.mirrorArrow())
        buttonstack.addWidget(self.mirrorButton)

        self.bringForward = QPushButton("Bring Forward")
        self.bringForward.clicked.connect(self.handlers.bringForward)
        buttonstack.addWidget(self.bringForward)

        self.swapColors = QPushButton("Swap Colors")
        self.swapColors.clicked.connect(self.handlers.swapColors)
        buttonstack.addWidget(self.swapColors)

        self.exportAsPNGButton = QPushButton("Export to PNG")
        self.exportAsPNGButton.clicked.connect(self.handlers.exportAsPng)
        buttonstack.addWidget(self.exportAsPNGButton)

        self.exportAsSVGButton = QPushButton("Export to SVG")
        self.exportAsSVGButton.clicked.connect(self.handlers.exportAsSvg)
        buttonstack.addWidget(self.exportAsSVGButton)

        button_font = QFont('Helvetica', 14)
        button_width = 200

        self.deleteButton.setFont(button_font)
        self.rotateRightButton.setFont(button_font)
        self.rotateLeftButton.setFont(button_font)
        self.mirrorButton.setFont(button_font)
        self.bringForward.setFont(button_font)
        self.swapColors.setFont(button_font)
        self.exportAsPNGButton.setFont(button_font)
        self.exportAsSVGButton.setFont(button_font)
        self.updatePositionButton.setFont(button_font)
        self.selectAllButton.setFont(button_font)
        add_to_sequence_button.setFont(button_font)

        self.deleteButton.setFixedWidth(button_width)
        self.rotateRightButton.setFixedWidth(button_width)
        self.rotateLeftButton.setFixedWidth(button_width)
        self.mirrorButton.setFixedWidth(button_width)
        self.bringForward.setFixedWidth(button_width)
        self.swapColors.setFixedWidth(button_width)
        self.exportAsPNGButton.setFixedWidth(button_width)
        self.exportAsSVGButton.setFixedWidth(button_width)
        self.updatePositionButton.setFixedWidth(button_width)
        self.selectAllButton.setFixedWidth(button_width)
        add_to_sequence_button.setFixedWidth(button_width)




        return masterbtnlayout

    def initLetterButtons(self, staff_manager):
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
                button = QPushButton(letter, self)
                font = QFont()
                font.setPointSize(20)
                button.setFont(font)
                button.setFixedSize(80, 80)
                button.clicked.connect(lambda _, l=letter: self.generatePictograph(l, staff_manager))  # pass staff_manager here
                row_layout.addWidget(button)
            letter_buttons_layout.addLayout(row_layout)
        
        return letter_buttons_layout

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.handlers.deleteArrow()

    def add_to_sequence(self, artboard, sequence_constructor):
        state = artboard.get_state()
        pictograph = Pictograph(state)
        sequence_constructor.add_pictograph(pictograph)
        artboard.deleteAllItems()

        self.sequence_scene = QGraphicsScene()

        for arrow_state in state['arrows']:
            arrow = Arrow(arrow_state['svg_file'], self, self.infoTracker, self.handlers)
            arrow.setPos(arrow_state['position'])
            arrow.setScale(0.5)  # Scale down the item
            self.sequence_scene.addItem(arrow)

        # Create a QGraphicsView for the new scene
        sequence_view = QGraphicsView(self.sequence_scene)

        # Add the new view to the sequence view
        self.sequence_scene.addWidget(sequence_view)


    def generatePictograph(self, letter, staff_manager):
        #delete all items
        self.artboard.deleteAllItems()

        # Reload the JSON file
        with open('letterCombinations.json', 'r') as file:
            self.letterCombinations = json.load(file)

        # Get the list of possible combinations for the letter
        combinations = self.letterCombinations.get(letter, [])
        if not combinations:
            print(f"No combinations found for letter {letter}")
            return

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
                arrow = Arrow(svg, self.artboard_view, self.infoTracker, self.handlers)
                arrow.attributesChanged.connect(lambda: self.update_staff(arrow, staff_manager))
                arrow.set_attributes(combination)
                arrow.setFlag(QGraphicsItem.ItemIsMovable, True)
                arrow.setFlag(QGraphicsItem.ItemIsSelectable, True)

                # Add the created arrow to the list
                created_arrows.append(arrow)

        # Add the arrows to the scene
        for arrow in created_arrows:
            self.scene.addItem(arrow)

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

        self.update_position_label()
        self.staff_manager.remove_non_beta_staves()
        # Update the info label
        self.infoTracker.update()
        self.artboard_view.arrowMoved.emit()

    def update_position_label(self):
        start_position, end_position = self.infoTracker.get_positions()
        self.position_label.setText(f"Start: {start_position}\nEnd: {end_position}")

    def update_staff(self, arrow, staff_manager):
        # Convert the arrow to a list if it's not already a list
        arrows = [arrow] if not isinstance(arrow, list) else arrow

        # Get the new staff positions from the arrows
        staff_positions = [arrow.end_location.upper() + '_staff_' + arrow.color for arrow in arrows]

        # Show and hide the staffs based on the staff positions
        for element_id, staff in staff_manager.staffs.items():
            if element_id in staff_positions:
                staff.show()
            else:
                staff.hide()

        # Check and replace the staves
        self.staff_manager.check_and_replace_staves()


    def loadLetters(self):
        try:
            with open('letterCombinations.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def saveLetters(self):
        # Sort the data alphabetically by keys
        sorted_data = {key: self.letterCombinations[key] for key in sorted(self.letterCombinations)}
        # Write to file in a pretty format
        with open('letterCombinations.json', 'w') as f:
            json.dump(sorted_data, f, indent=4)
            
    def assignLetter(self):
        letter = self.letterInput.text().upper()
        if letter not in letter_positions:
            print(f"{letter} is not a valid letter.")
            return
        selected_items = self.artboard.selectedItems()
        if len(selected_items) != 2 or not all(isinstance(item, Arrow) for item in selected_items):
            print("Please select a combination of two arrows.")
            return
        letter_instance = Letter(selected_items[0], selected_items[1])
        letter_instance.assign_letter(letter)
        arrow_combination = [item.get_attributes() for item in selected_items]
        variations = generate_variations(arrow_combination)
        print(f"Generated {len(variations)} variations for the selected combination of arrows.")
        print(f"{variations}")
        if letter not in self.letterCombinations:
            self.letterCombinations[letter] = []
        for variation in variations:
            self.letterCombinations[letter].append(variation)
        self.letterCombinations[letter].sort(key=lambda x: (x[0]['color'], x[1]['color']))  # add this line to sort variations

        print(f"Assigned {letter} to the selected combination of arrows and all its variations.")
        self.infoTracker.update()

    def loadSvg(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open SVG", "", "SVG files (*.svg)")
        if fileName:
            self.svgWidget.load(fileName)

class Letter:
    def __init__(self, arrow1, arrow2):
        self.arrow1 = arrow1
        self.arrow2 = arrow2
        self.letter = None  # Add an attribute for the letter
        
    def get_start_location(self):
        # Get the start positions of the two arrows
        start_location1 = Arrow.get_arrow_start_location(self.arrow1)
        start_location2 = Arrow.get_arrow_start_location(self.arrow2)
        print("start positions: ", start_location1, start_location2)

        # Return the position corresponding to the pair of start positions
        return Arrow.get_position_from_directions(start_location1, start_location2)
        
    def get_end_location(self):
        # Get the end positions of the two arrows
        end_location1 = Arrow.get_arrow_end_location(self.arrow1)
        end_location2 = Arrow.get_arrow_end_location(self.arrow2)
        print("end positions: ", end_location1, end_location2)

        # Return the position corresponding to the pair of end positions
        return Arrow.get_position_from_directions(end_location1, end_location2)

    def assign_letter(self, letter):
        # Check if the start and end positions match the positions for the letter
        if (self.get_start_location(), self.get_end_location()) == letter_positions[letter]:
            self.letter = letter  # Assign the letter
            print(f"Assigned {letter} to the letter.")
        else:
            print(f"The start and end positions do not match the positions for {letter}.")

    def update_letter(self):
        current_combination = []

        for item in self.artboard.items():
            if isinstance(item, Arrow):
                attributes = item.get_attributes()
                current_combination.append(attributes)

        current_combination = sorted(current_combination, key=lambda x: x['color'])

        for letter, combinations in self.letterCombinations.items():
            combinations = [sorted(combination, key=lambda x: x['color']) for combination in combinations]
            if current_combination in combinations:
                return letter  # Return the letter if the current combination matches

        return None  # Return None if no match is found

app = QApplication(sys.argv)
ex = Main_Window()
ex.setFocus()  
sys.exit(app.exec_())