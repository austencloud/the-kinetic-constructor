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
from sequence import *
from buttons import Button_Manager
from generator import *

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
        self.word_label = QLabel(self)
        self.staff_manager = StaffManager(self.scene)
        self.info_tracker = Info_Tracker(None, self.info_label, self, self.staff_manager)
        self.artboard = Artboard(self.scene, self.grid, self.info_tracker, self.staff_manager)
        self.artboard_view = self.initArtboard() 
        self.sequence_scene = Sequence_Scene()  # Create a new Sequence_Scene instance
        self.handlers = Handlers(self.artboard, self.artboard_view, self.grid, self.artboard, self.info_tracker, self)
        self.pictograph_generator = Pictograph_Generator(self.staff_manager, self.artboard, self.artboard_view, self.scene, self.info_tracker, self.handlers, self)
        self.sequence_manager = Sequence_Manager(self.sequence_scene, self.pictograph_generator, self, self.info_tracker)
        self.button_manager = Button_Manager()
        self.button_layot = self.button_manager.initButtons(self.artboard, self.artboard_view, self.grid,self.info_tracker, self.sequence_manager)
        self.initUI()

        self.letters = self.loadLetters()
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
        lower_right_layout = QVBoxLayout()
        artboard_layout = QVBoxLayout()
        button_layout = QVBoxLayout()
        info_layout = QVBoxLayout()
        upper_right_laybout.addLayout(button_layout)
        upper_right_laybout.addLayout(artboard_layout)
        upper_right_laybout.addLayout(self.button_layot)
        upper_right_laybout.addLayout(info_layout)
        right_layout.addLayout(upper_right_laybout)
        right_layout.addLayout(lower_right_layout)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        # set the letter buttons
        letter_buttons_layout = self.pictograph_generator.initLetterButtons()
        left_layout.addLayout(letter_buttons_layout)

        # set the artboard
        self.info_tracker.set_artboard(self.artboard)
        artboard_layout.addWidget(self.artboard_view)

        #set up the arrowbox
        arrowbox = self.initArrowBox()
        left_layout.addWidget(arrowbox)

        # set the buttons and info tracker
        info_layout.addWidget(self.info_label)
        upper_right_laybout.addLayout(button_layout)
        upper_right_laybout.addLayout(info_layout) 
        self.scene.changed.connect(self.info_tracker.update)
        
        lower_right_layout.addWidget(self.word_label)
        self.word_label.setFont(QFont('Helvetica', 20))
        self.word_label.setText("My word: ")
        self.sequence_manager.initSequenceScene(lower_right_layout, self.sequence_scene)

        clear_sequence_button = self.sequence_manager.get_clear_sequence_button()
        lower_right_layout.addWidget(clear_sequence_button)

        ### Un-comment this code to enable the assign letter funtion ###
        # self.letterInput = QLineEdit(self)
        # right_layout.addWidget(self.letterInput)
        # self.assignLetterButton = QPushButton("Assign Letter", self)
        # self.assignLetterButton.clicked.connect(self.assignLetter)
        # right_layout.addWidget(self)

        self.setMinimumSize(2800, 1400)
        self.show()

    def initArrowBox(self):
        arrow_box = QScrollArea(self)
        arrowbox_scene = QGraphicsScene()
        for arrow in self.arrows:
            arrowbox_scene.addItem(arrow)  # use arrowbox_scene here
            arrow.attributesChanged.connect(self.info_tracker.update)
            arrow.attributesChanged.connect(lambda: self.update_staff(arrow, self.staff_manager))

        svgs_full_paths = []
        default_arrows = ['red_anti_r_ne.svg', 'red_iso_r_ne.svg', 'blue_anti_r_sw.svg', 'blue_iso_r_sw.svg']
        svg_item_count = 0

        for dirpath, dirnames, filenames in os.walk(self.ARROW_DIR):
            svgs_full_paths.extend([os.path.join(dirpath, filename) for filename in filenames if filename.endswith('.svg')])

        for i, svg in enumerate(svgs_full_paths):
            file_name = os.path.basename(svg)
            if file_name in default_arrows:
                self.artboard.set_handlers(self.handlers)
                arrow_item = Arrow(svg, self.artboard_view, self.info_tracker, self.handlers)
                arrow_item.setFlag(QGraphicsItem.ItemIsMovable, True)
                arrow_item.setFlag(QGraphicsItem.ItemIsSelectable, True)
                arrow_item.setScale(1)
                arrow_item.setPos(0, svg_item_count * self.SVG_POS_Y)
                arrowbox_scene.addItem(arrow_item) 
                arrow_item.attributesChanged.connect(self.info_tracker.update)

                svg_item_count += 1
                self.arrows.append(arrow_item)

        view = QGraphicsView(arrowbox_scene)
        view.setFrameShape(QFrame.NoFrame)
        arrow_box.setWidget(view)
        arrow_box.setWidgetResizable(True)
        arrow_box.setFixedSize(500, 1400)

        return arrow_box

    def initArtboard(self):
        self.artboard.setFixedSize(750, 750)

        transform = QTransform()
        self.grid_center = QPointF(self.artboard.frameSize().width() / 2, self.artboard.frameSize().height() / 2)


        self.artboard.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.artboard.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene.addItem(self.grid)

        return self.artboard

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.handlers.deleteArrow()

    def loadLetters(self):
        try:
            with open('letters.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def saveLetters(self):
        sorted_data = {key: self.letters[key] for key in sorted(self.letters)}
        with open('letters.json', 'w') as f:
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
        if letter not in self.letters:
            self.letters[letter] = []
        for variation in variations:
            self.letters[letter].append(variation)
        self.letters[letter].sort(key=lambda x: (x[0]['color'], x[1]['color']))

        print(f"Assigned {letter} to the selected combination of arrows and all its variations.")
        self.info_tracker.update()

    def loadSvg(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open SVG", "", "SVG files (*.svg)")
        if fileName:
            self.svgWidget.load(fileName)
class Letter:
    def __init__(self, arrow1, arrow2):
        self.arrow1 = arrow1
        self.arrow2 = arrow2
        self.letter = None
        
    def get_start_location(self):
        start_location1 = Arrow.get_arrow_start_location(self.arrow1)
        start_location2 = Arrow.get_arrow_start_location(self.arrow2)
        print("start positions: ", start_location1, start_location2)

        return Arrow.get_position_from_directions(start_location1, start_location2)
        
    def get_end_location(self):
        end_location1 = Arrow.get_arrow_end_location(self.arrow1)
        end_location2 = Arrow.get_arrow_end_location(self.arrow2)
        print("end positions: ", end_location1, end_location2)


        return Arrow.get_position_from_directions(end_location1, end_location2)

    def assign_letter(self, letter):
        if (self.get_start_location(), self.get_end_location()) == letter_positions[letter]:
            self.letter = letter
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

        for letter, combinations in self.letters.items():
            combinations = [sorted(combination, key=lambda x: x['color']) for combination in combinations]
            if current_combination in combinations:
                return letter

        return None

app = QApplication(sys.argv)
ex = Main_Window()
ex.setFocus()  
sys.exit(app.exec_())