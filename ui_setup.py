from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QScrollArea, QGraphicsScene, QGraphicsView, QGraphicsItem, QLabel, QFileDialog, QFrame, QWidget, QLineEdit
import os
from arrow import Arrow
from PyQt5.QtGui import QFont, QTransform
from sequence import *
from handlers import Handlers
from info_tracker import Info_Tracker
from generator import Pictograph_Generator
from staff import Staff_Manager
from letter import Letter_Manager

class UiSetup(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)

        self.main_window = main_window
        self.main_window.setMinimumSize(2800, 1400)
        self.main_window.show()

        self.arrows = []
        self.artboard_scene = QGraphicsScene()
        self.ARROW_DIR = 'images\\arrows'
        self.SVG_POS_Y = 250

    def initLayouts(self):
        self.main_layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()
        self.left_layout = QHBoxLayout()
        self.upper_right_layout = QHBoxLayout()
        self.lower_right_layout = QVBoxLayout()
        self.artboard_layout = QVBoxLayout()
        self.button_layout = QVBoxLayout()
        self.info_layout = QVBoxLayout()
        self.upper_right_layout.addLayout(self.artboard_layout)
        self.upper_right_layout.addLayout(self.button_layout)
        self.upper_right_layout.addLayout(self.info_layout)
        self.right_layout.addLayout(self.upper_right_layout)
        self.right_layout.addLayout(self.lower_right_layout)
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        self.main_window.setLayout(self.main_layout)

    def initArtboard(self):
        self.grid = Grid('images\\grid\\grid.svg')
        self.artboard = Artboard(self.artboard_scene, self.grid, self.info_tracker, self.staff_manager)
        self.artboard_view = self.artboard.initArtboard() 
        transform = QTransform()
        self.grid_center = QPointF(self.artboard.frameSize().width() / 2, self.artboard.frameSize().height() / 2)
        grid_size = 650
        transform.translate(self.grid_center.x() - (grid_size / 2), self.grid_center.y() - (grid_size / 2))
        self.grid.setTransform(transform)

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
                button = QPushButton(letter, self.main_window)
                font = QFont()
                font.setPointSize(20)
                button.setFont(font)
                button.setFixedSize(80, 80)
                button.clicked.connect(lambda _, l=letter: self.pictograph_generator.generate_pictograph(l, self.staff_manager))  # use self.pictograph_generator here
                row_layout.addWidget(button)
            letter_buttons_layout.addLayout(row_layout)
        
        self.left_layout.addLayout(letter_buttons_layout)  # add the layout to left_layout here

    def initButtons(self):
        button_font = QFont('Helvetica', 14)
        button_width = 225
    
        self.artboard.set_handlers(self.handlers)
        masterbtnlayout = QVBoxLayout()
        buttonlayout = QHBoxLayout()
        buttonstack = QVBoxLayout()
        buttonstack.setAlignment(Qt.AlignTop)
        masterbtnlayout.setAlignment(Qt.AlignTop)
        buttonlayout.addLayout(buttonstack)
        masterbtnlayout.addLayout(buttonlayout)

        self.updatePositionButton = QPushButton("Update Position")
        self.updatePositionButton.clicked.connect(lambda: self.handlers.updatePositionInJson(*self.artboard.get_current_arrow_positions()))
        buttonstack.addWidget(self.updatePositionButton)

        self.selectAllButton = QPushButton("Select All")
        self.selectAllButton.clicked.connect(self.handlers.selectAll)
        buttonstack.addWidget(self.selectAllButton)

        add_to_sequence_button = QPushButton("Add to Sequence")
        add_to_sequence_button.clicked.connect(lambda _: self.sequence_manager.add_to_sequence(self.artboard))
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

        self.button_layout.addLayout(masterbtnlayout)

    def initArrowBox(self):
        arrow_box = QScrollArea(self.main_window)
        arrowbox_scene = QGraphicsScene()
        for arrow in self.arrows:
            arrowbox_scene.addItem(arrow)  # use arrowbox_scene here
            arrow.attributesChanged.connect(self.info_tracker.update)
            arrow.attributesChanged.connect(lambda: self.pictograph_generator.update_staff(arrow, self.staff_manager))

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

        self.left_layout.addWidget(arrow_box)

    def initInfoTracker(self):
        self.info_label = QLabel(self.main_window)
        self.info_tracker = Info_Tracker(None, self.info_label, self, self.staff_manager)

    def initWordLabel(self):
        self.word_label = QLabel(self.main_window)
        self.lower_right_layout.addWidget(self.word_label)
        self.word_label.setFont(QFont('Helvetica', 20))
        self.word_label.setText("My word: ")

    def initSequenceScene(self):
        self.sequence_scene = Sequence_Scene()  # Create a new Sequence_Scene instance
        self.sequence_manager = Sequence_Manager(self.sequence_scene, self.pictograph_generator, self, self.info_tracker)

        self.sequence_scene.set_manager(self.sequence_manager)  # Set the manager of the sequence container
        self.sequence_manager.manager = self.sequence_manager  # Set the manager of the sequence scene

        self.sequence_container = QGraphicsView(self.sequence_scene)  # Create a QGraphicsView with the sequence scene

        # Set the width and height
        self.sequence_container.setFixedSize(1700, 500)
        self.sequence_container.show()
        self.lower_right_layout.addWidget(self.sequence_container)

        clear_sequence_button = self.sequence_manager.get_clear_sequence_button()
        self.lower_right_layout.addWidget(clear_sequence_button)

    def initHandlers(self):
       self.handlers = Handlers(self.artboard, self.artboard_view, self.grid, self.artboard, self.info_tracker, self)
       self.artboard.set_handlers(self.handlers)

    def initGenerator(self):
        self.pictograph_generator = Pictograph_Generator(self.staff_manager, self.artboard, self.artboard_view, self.artboard_scene, self.info_tracker, self.handlers, self.main_window, self)

    def initStaffManager(self):
        self.staff_manager = Staff_Manager(self.artboard_scene)

    def connectInfoTracker(self):
        self.info_layout.addWidget(self.info_label)

        self.artboard_scene.changed.connect(self.info_tracker.update)

    def connectArtboard(self):
        self.info_tracker.set_artboard(self.artboard)
        self.artboard_layout.addWidget(self.artboard_view)

    def initLetterManager(self):
        self.letter_manager = Letter_Manager(self.artboard, self.info_tracker)
        self.letterInput = QLineEdit(self.main_window)
        self.right_layout.addWidget(self.letterInput)
        self.assignLetterButton = QPushButton("Assign Letter", self.main_window)
        self.assignLetterButton.clicked.connect(lambda: self.letter_manager.assignLetter(self.letterInput.text()))
        self.right_layout.addWidget(self.assignLetterButton)

    def keyPressEvent(self, event):
        self.handlers.handleKeyPressEvent(event)