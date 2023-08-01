from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QScrollArea, QGraphicsScene, QGraphicsView, QGraphicsItem, QLabel, QFrame, QWidget, QLineEdit
import os
from arrow import Arrow
from PyQt5.QtGui import QFont, QTransform
from sequence import *
from handlers import Handlers
from info_tracker import Info_Tracker
from generator import Pictograph_Generator
from staff import *
from letter import Letter_Manager
from PyQt5.QtCore import Qt, QPointF, QEvent
from handlers import Arrow_Manipulator, SvgHandler, Exporter, JsonUpdater
from arrowbox import Arrow_Box
from propbox import Prop_Box
from menus import Menu_Bar, Context_Menu_Handler
from graphboard import Graphboard

class UiSetup(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setFocusPolicy(Qt.StrongFocus)
        self.main_window = main_window
        self.main_window.installEventFilter(self)  # This allows the main window to receive key events
        self.main_window.setMinimumSize(2900, 1600)
        self.main_window.show()
        self.svg_handler = SvgHandler()
        self.arrows = []
        self.graphboard_scene = QGraphicsScene()
        self.ARROW_DIR = 'images\\arrows'
        self.SVG_POS_Y = 250
        self.context_menu_handler = None
        self.exporter = None
        self.handlers = None
        self.sequence_manager = None
        self.graphboard = None
        self.arrow_manipulator = None

        self.initStaffManager()
        self.initLayouts()
        self.initInfoTracker()
        self.initMenus()
        self.initGraphboard()

        self.connectGraphboard()
        self.initHandlers()
        self.initLetterButtons()
        self.initArrowBox()
        self.initGenerator()
        self.initPropBox()
        self.initButtons()
        self.connectInfoTracker()
        self.initWordLabel()
        self.initSequenceScene()
        self.setFocus()



    def initMenus(self):
        self.exporter = Exporter(self.graphboard, self.graphboard_scene)
        self.json_updater = JsonUpdater(self.graphboard_scene)
        self.context_menu_handler = Context_Menu_Handler(self.graphboard_scene, self.handlers, self.sequence_manager, self.arrow_manipulator, self.exporter)
        self.menu_bar = Menu_Bar()

    def initLayouts(self):
        self.main_layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()
        self.left_layout = QHBoxLayout()
        self.top_right_layout = QHBoxLayout() # graphboard, buttons, info
        #align the top right layout ot he right
        self.bottom_right_layout = QVBoxLayout() # Sequence
        self.lower_top_right_layout = QHBoxLayout() # Word label
        self.graphboard_layout = QVBoxLayout()
        self.graphboard_layout.setAlignment(Qt.AlignRight)
        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignRight)
        self.info_layout = QVBoxLayout()
        self.info_layout.setAlignment(Qt.AlignRight)
        self.word_label_layout = QHBoxLayout()


        self.top_right_layout.addLayout(self.graphboard_layout)
        self.top_right_layout.addLayout(self.button_layout)
        self.top_right_layout.addLayout(self.info_layout)

        self.lower_top_right_layout.addLayout(self.word_label_layout)
        self.bottom_right_layout.addLayout(self.lower_top_right_layout)

        self.right_layout.addLayout(self.top_right_layout)
        self.right_layout.addLayout(self.bottom_right_layout)


        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        self.main_window.setLayout(self.main_layout)

    def initGraphboard(self):
        self.grid = Grid('images\\grid\\grid.svg')
        self.graphboard = Graphboard(self.graphboard_scene, self.grid, self.info_tracker, self.staff_manager, self.svg_handler, self)
        transform = QTransform()
        self.grid_center = QPointF(self.graphboard.frameSize().width() / 2, self.graphboard.frameSize().height() / 2 - 75)
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
                button.clicked.connect(lambda _, l=letter: self.generator.generate_pictograph(l, self.staff_manager))  # use self.generator here
                row_layout.addWidget(button)
            letter_buttons_layout.addLayout(row_layout)
        
        self.left_layout.addLayout(letter_buttons_layout)  # add the layout to left_layout here
    
    def initButtons(self):
        button_font = QFont('Helvetica', 14)
        button_width = 225

        self.graphboard.set_handlers(self.handlers)
        masterbtnlayout = QVBoxLayout()
        buttonlayout = QHBoxLayout()
        buttonstack = QVBoxLayout()
        buttonstack.setAlignment(Qt.AlignTop)
        masterbtnlayout.setAlignment(Qt.AlignTop)
        buttonlayout.addLayout(buttonstack)
        masterbtnlayout.addLayout(buttonlayout)

        ### DEVELOPER FUNCTIONS ###

        self.updatePositionButton = QPushButton("Update Position")
        self.updatePositionButton.clicked.connect(lambda: self.json_updater.updatePositionInJson(*self.graphboard.getCurrentArrowPositions()))
        buttonstack.addWidget(self.updatePositionButton)

        ### ARROW MANIPULATOR BUTTONS ###

        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(lambda: self.handlers.arrowManipulator.delete_arrow(self.graphboard_scene.selectedItems()))
        buttonstack.addWidget(self.deleteButton)

        self.rotateRightButton = QPushButton("Rotate Right")
        self.rotateRightButton.clicked.connect(lambda: self.handlers.arrowManipulator.rotateArrow("right", self.graphboard_scene.selectedItems()))
        buttonstack.addWidget(self.rotateRightButton)

        self.rotateLeftButton = QPushButton("Rotate Left")
        self.rotateLeftButton.clicked.connect(lambda: self.handlers.arrowManipulator.rotateArrow("left", self.graphboard_scene.selectedItems()))
        buttonstack.addWidget(self.rotateLeftButton)

        self.mirrorButton = QPushButton("Mirror")
        self.mirrorButton.clicked.connect(lambda: self.handlers.arrowManipulator.mirrorArrow(self.graphboard_scene.selectedItems()))
        buttonstack.addWidget(self.mirrorButton)

        self.bringForward = QPushButton("Bring Forward")
        self.bringForward.clicked.connect(lambda: self.handlers.arrowManipulator.bringForward(self.graphboard_scene.selectedItems()))
        buttonstack.addWidget(self.bringForward)

        self.swapColors = QPushButton("Swap Colors")
        self.swapColors.clicked.connect(lambda: self.handlers.arrowManipulator.swapColors(self.graphboard_scene.selectedItems()))
        buttonstack.addWidget(self.swapColors)

        ### SELECTION BUTTONS ###

        self.selectAllButton = QPushButton("Select All")
        self.selectAllButton.clicked.connect(self.handlers.arrowManipulator.selectAll)
        buttonstack.addWidget(self.selectAllButton)

        ### SEQUENCE BUTTONS ###

        add_to_sequence_button = QPushButton("Add to Sequence")
        add_to_sequence_button.clicked.connect(lambda _: self.sequence_manager.add_to_sequence(self.graphboard))
        buttonstack.addWidget(add_to_sequence_button)

        ### EXPORT BUTTONS ###

        self.exportAsPNGButton = QPushButton("Export to PNG")
        self.exportAsPNGButton.clicked.connect(self.handlers.exporter.exportAsPng)
        buttonstack.addWidget(self.exportAsPNGButton)

        self.exportAsSVGButton = QPushButton("Export to SVG")
        self.exportAsSVGButton.clicked.connect(self.handlers.exporter.exportAsSvg)
        buttonstack.addWidget(self.exportAsSVGButton)
        
        ### STYLING ###

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
        arrowbox_frame = QFrame(self.main_window)
        arrowbox_layout = QVBoxLayout()  # create a layout
        arrowbox_frame.setLayout(arrowbox_layout)  # set the layout to the frame

        arrowbox_scene = QGraphicsScene()
        self.arrow_manipulator = Arrow_Manipulator(self.graphboard_scene, self.graphboard)
        for arrow in self.arrows:
            arrowbox_scene.addItem(arrow)  # use arrowbox_scene here
            arrow.attributesChanged.connect(self.info_tracker.update)
            arrow.attributesChanged.connect(lambda: self.generator.update_staff(arrow, self.staff_manager))

        svgs_full_paths = []
        default_arrows = ['red_anti_r_ne.svg', 'red_iso_r_ne.svg', 'blue_anti_r_sw.svg', 'blue_iso_r_sw.svg']
        svg_item_count = 0

        for dirpath, dirnames, filenames in os.walk(self.ARROW_DIR):
            svgs_full_paths.extend([os.path.join(dirpath, filename) for filename in filenames if filename.endswith('.svg')])

        for i, svg_file in enumerate(svgs_full_paths):
            file_name = os.path.basename(svg_file)
            if file_name in default_arrows:
                self.graphboard.set_handlers(self.arrow_manipulator)
                arrow_item = Arrow(svg_file, self.graphboard, self.info_tracker, self.svg_handler, self.arrow_manipulator)
                arrow_item.setFlag(QGraphicsItem.ItemIsMovable, True)
                arrow_item.setFlag(QGraphicsItem.ItemIsSelectable, True)
                arrow_item.setScale(1)
                arrow_item.setPos(0, svg_item_count * self.SVG_POS_Y)
                arrowbox_scene.addItem(arrow_item) 
                print(self.info_tracker)
                arrow_item.attributesChanged.connect(self.info_tracker.update)

                svg_item_count += 1
                self.arrows.append(arrow_item)

        arrowbox = Arrow_Box(arrowbox_scene, self.graphboard, self.info_tracker, self.svg_handler)

        arrowbox_layout.addWidget(arrowbox) 
        arrowbox_frame.setFixedSize(400, 1200)
        self.left_layout.addWidget(arrowbox_frame)

    def initPropBox(self):
        self.prop_box = Prop_Box(self.main_window, self.staff_manager, self)

    def initInfoTracker(self):
        self.info_label = QLabel(self.main_window)
        self.info_tracker = Info_Tracker(None, self.info_label, self, self.staff_manager)

    def initWordLabel(self):
        self.word_label = QLabel(self.main_window)
        self.bottom_right_layout.addWidget(self.word_label)
        self.word_label.setFont(QFont('Helvetica', 20))
        self.word_label.setText("My word: ")

    def initSequenceScene(self):
        self.sequence_scene = Sequence_Scene()  # Create a new Sequence_Scene instance
        self.sequence_manager = Sequence_Manager(self.sequence_scene, self.generator, self, self.info_tracker)

        self.sequence_scene.set_manager(self.sequence_manager)  # Set the manager of the sequence container
        self.sequence_manager.manager = self.sequence_manager  # Set the manager of the sequence scene

        self.sequence_container = QGraphicsView(self.sequence_scene)  # Create a QGraphicsView with the sequence scene

        # Set the width and height
        self.sequence_container.setFixedSize(1700, 500)
        self.sequence_container.show()
        self.bottom_right_layout.addWidget(self.sequence_container)

        clear_sequence_button = self.sequence_manager.get_clear_sequence_button()
        self.bottom_right_layout.addWidget(clear_sequence_button)

    def initHandlers(self):
       self.handlers = Handlers(self.graphboard, self.graphboard, self.grid, self.graphboard, self.info_tracker, self)
       self.graphboard.set_handlers(self.handlers)

    def initGenerator(self):
        self.generator = Pictograph_Generator(self.staff_manager, self.graphboard, self.graphboard, self.graphboard_scene, self.info_tracker, self.handlers, self.main_window, self, self.arrow_manipulator)

    def initStaffManager(self):
        self.staff_manager = Staff_Manager(self.graphboard_scene)

    def initLetterManager(self):
        self.letter_manager = Letter_Manager(self.graphboard, self.info_tracker)
        self.letterInput = QLineEdit(self.main_window)
        self.right_layout.addWidget(self.letterInput)
        self.assignLetterButton = QPushButton("Assign Letter", self.main_window)
        self.assignLetterButton.clicked.connect(lambda: self.letter_manager.assignLetter(self.letterInput.text()))
        self.right_layout.addWidget(self.assignLetterButton)


### CONNECTORS ###


    def connectInfoTracker(self):
        self.info_layout.addWidget(self.info_label)

        self.graphboard_scene.changed.connect(self.info_tracker.update)

    def connectGraphboard(self):
        self.info_tracker.set_graphboard(self.graphboard)
        self.graphboard_layout.addWidget(self.graphboard)


### GETTERS ###

    def get_sequence_manager(self):
        if not hasattr(self, 'sequence_manager'):
            self.sequence_manager = Sequence_Manager(self.sequence_scene, self.generator, self, self.info_tracker)
            self.sequence_scene.set_manager(self.sequence_manager)  # Set the manager of the sequence container
            self.sequence_manager.manager = self.sequence_manager  # Set the manager of the sequence scene
        return self.sequence_manager


### EVENTS ###

    def keyPressEvent(self, event):
        self.handlers.keyPressHandler.handleKeyPressEvent(event)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            self.keyPressEvent(event)
            return True
        return super().eventFilter(source, event)