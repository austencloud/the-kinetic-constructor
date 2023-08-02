from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QScrollArea, QGraphicsScene, QGraphicsView, QGraphicsItem, QLabel, QFrame, QWidget, QLineEdit, QGridLayout
import os
from arrow import Arrow
from PyQt5.QtGui import QFont, QTransform, QIcon
from sequence import *
from info_tracker import Info_Tracker
from generator import Pictograph_Generator
from staff import *
from letter import Letter_Manager
from PyQt5.QtCore import Qt, QPointF, QEvent, QSize
from handlers import Arrow_Handler, Svg_Handler, Exporter, Json_Handler, Key_Press_Handler
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
        self.main_window.setMinimumSize(2000, 1600)
        self.main_window.show()
        #set title of main window
        self.main_window.setWindowTitle("Sequence Generator")
        self.svg_handler = Svg_Handler()
        self.arrows = []
        self.graphboard_scene = QGraphicsScene()
        self.ARROW_DIR = 'images\\arrows'
        self.SVG_POS_Y = 250
        self.context_menu_handler = None
        self.exporter = None
        self.handlers = None
        self.sequence_manager = None
        self.graphboard = None
        self.arrow_handler = None

        self.initStaffManager()
        self.initLayouts()
        self.initInfoTracker()
        self.initMenus()
        self.initGraphboard()  # Initialize graphboard first
        self.initGenerator()  # Then initialize generator
        self.graphboard.setGenerator(self.generator)  # Update graphboard with generator

        self.connectGraphboard()


        self.initArrowBox()

        self.initPropBox()
        self.initButtons()
        self.connectInfoTracker()
        self.initWordLabel()
        self.initSequenceScene()
        self.initLetterButtons()  # Move this line down
        self.setFocus()


    def initMenus(self):
        self.json_updater = Json_Handler(self.graphboard_scene)
        self.context_menu_handler = Context_Menu_Handler(self.graphboard_scene, self.handlers, self.sequence_manager, self.arrow_handler, self.exporter)
        self.arrow_handler = Arrow_Handler(self.graphboard_scene, self.graphboard)
        self.key_press_handler = Key_Press_Handler(self.arrow_handler, None)
        self.menu_bar = Menu_Bar()

    def initLayouts(self):
        self.main_layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()  # Change this to QHBoxLayout
        self.upper_layout = QHBoxLayout()  # This will contain graphboard and buttons
        self.lower_layout = QVBoxLayout()  # Sequence
        self.top_of_lower_layout = QHBoxLayout()


        self.objectbox_layout = QVBoxLayout()

        self.graphboard_layout = QVBoxLayout()

        self.button_layout = QHBoxLayout()  # Change this to QHBoxLayout

        self.info_layout = QVBoxLayout()

        self.word_label_layout = QHBoxLayout()



        self.upper_graphboard_with_panel_layout = QVBoxLayout()
        self.upper_graphboard_with_panel_layout.addLayout(self.graphboard_layout)
        self.upper_graphboard_with_panel_layout.addLayout(self.button_layout)  # Add button_layout after graphboard_layout
        
        self.upper_layout.addLayout(self.objectbox_layout)
        self.upper_layout.addLayout(self.upper_graphboard_with_panel_layout)
        self.upper_layout.addStretch()

        self.objectbox_layout.addStretch()
        self.objectbox_layout.addStretch()


        self.top_of_lower_layout.addLayout(self.word_label_layout)
        self.lower_layout.addLayout(self.top_of_lower_layout)

        self.right_layout.addLayout(self.upper_layout)
        self.upper_layout.addLayout(self.info_layout)
        self.right_layout.addLayout(self.lower_layout)  # Add info_layout to right_layout

        self.main_layout.addLayout(self.right_layout)
        self.main_window.setLayout(self.main_layout)


    def initGraphboard(self):
        self.grid = Grid('images\\grid\\grid.svg')
        self.exporter = Exporter(self.graphboard, self.graphboard_scene, self.staff_manager, self.grid)
        # Initialize graphboard without generator
        self.graphboard = Graphboard(self.graphboard_scene, self.grid, self.info_tracker, self.staff_manager, self.svg_handler, self, None, self.sequence_manager)
        self.key_press_handler.connect_to_graphboard(self.graphboard)
        self.arrow_handler.connect_to_graphboard(self.graphboard)
        transform = QTransform()

        # Get the size of the graphboard
        graphboard_size = self.graphboard.frameSize()

        # Calculate the position of the grid
        grid_position = QPointF((graphboard_size.width() - self.grid.boundingRect().width()) / 2,
                                (graphboard_size.height() - self.grid.boundingRect().height()) / 2 - 75)

        transform.translate(grid_position.x(), grid_position.y())
        self.grid.setTransform(transform)
        
    def initLetterButtons(self):
        # Create a new layout for the Word Constructor's widgets
        letter_buttons_layout = QVBoxLayout()
        letter_buttons_layout.setSpacing(10)  # Set the spacing between rows of buttons
        letter_buttons_layout.setAlignment(Qt.AlignTop)  # Align the layout to the top

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
            row_layout.setSpacing(10)  # Set the spacing between buttons in a row
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
        
        self.upper_layout.addLayout(letter_buttons_layout)  # add the layout to left_layout here

    def initButtons(self):
        button_font = QFont('Helvetica', 14)
        button_width = 60
        button_height = 60
        icon_size = QSize(40, 40)

        self.graphboard.set_handlers(self.handlers)
        masterbtnlayout = QVBoxLayout()
        buttonlayout = QHBoxLayout()
        buttonstack = QHBoxLayout()
        buttonstack.setAlignment(Qt.AlignTop)
        masterbtnlayout.setAlignment(Qt.AlignTop)
        buttonlayout.addLayout(buttonstack)
        masterbtnlayout.addLayout(buttonlayout)

        ### DEVELOPER FUNCTIONS ###

        self.updatePositionButton = QPushButton(QIcon("images/icons/update_locations.png"), "")
        self.updatePositionButton.setToolTip("Update Position")
        self.updatePositionButton.clicked.connect(lambda: self.json_updater.updatePositionInJson(*self.graphboard.getCurrentArrowPositions()))

        ### ARROW MANIPULATOR BUTTONS ###

        self.deleteButton = QPushButton(QIcon("images/icons/delete.png"), "")
        self.deleteButton.setToolTip("Delete")
        self.deleteButton.clicked.connect(lambda: self.arrow_handler.delete_arrow(self.graphboard_scene.selectedItems()))
        

        self.rotateRightButton = QPushButton(QIcon("images/icons/rotate-right.png"), "")
        self.rotateRightButton.setToolTip("Rotate Right")
        self.rotateRightButton.clicked.connect(lambda: self.arrow_handler.rotateArrow("right", self.graphboard_scene.selectedItems()))
        self.rotateLeftButton = QPushButton(QIcon("images/icons/rotate-left.png"), "")
        self.rotateLeftButton.setToolTip("Rotate Left")
        self.rotateLeftButton.clicked.connect(lambda: self.arrow_handler.rotateArrow("left", self.graphboard_scene.selectedItems()))

        self.mirrorButton = QPushButton(QIcon("images/icons/mirror.png"), "")
        self.mirrorButton.setToolTip("Mirror")
        self.mirrorButton.clicked.connect(lambda: self.arrow_handler.mirrorArrow(self.graphboard_scene.selectedItems()))


        self.bringForward = QPushButton(QIcon("images/icons/bring_forward.png"), "")
        self.bringForward.setToolTip("Bring Forward")
        self.bringForward.clicked.connect(lambda: self.arrow_handler.bringForward(self.graphboard_scene.selectedItems()))

        self.swapColors = QPushButton(QIcon("images/icons/swap.png"), "")
        self.swapColors.setToolTip("Swap Colors")
        self.swapColors.clicked.connect(lambda: self.arrow_handler.swapColors(self.graphboard_scene.selectedItems()))

        ### SELECTION BUTTONS ###

        self.selectAllButton = QPushButton(QIcon("images/icons/select_all.png"), "")
        self.selectAllButton.setToolTip("Select All")
        self.selectAllButton.clicked.connect(self.arrow_handler.selectAll)


        ### SEQUENCE BUTTONS ###

        add_to_sequence_button = QPushButton(QIcon("images/icons/add_to_sequence.png"), "")
        add_to_sequence_button.setToolTip("Add to Sequence")
        add_to_sequence_button.clicked.connect(lambda _: self.sequence_manager.add_to_sequence(self.graphboard))


        ### EXPORT BUTTONS ###

        self.exportAsPNGButton = QPushButton(QIcon("images/icons/export.png"), "")
        self.exportAsPNGButton.setToolTip("Export to PNG")
        self.exportAsPNGButton.clicked.connect(self.exporter.exportAsPng)


        self.exportAsSVGButton = QPushButton(QIcon("images/icons/export.png"), "")
        self.exportAsSVGButton.setToolTip("Export to SVG")
        self.exportAsSVGButton.clicked.connect(self.exporter.exportAsSvg)


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

        self.deleteButton.setFixedHeight(button_height)
        self.rotateRightButton.setFixedHeight(button_height)
        self.rotateLeftButton.setFixedHeight(button_height)
        self.mirrorButton.setFixedHeight(button_height)
        self.bringForward.setFixedHeight(button_height)
        self.swapColors.setFixedHeight(button_height)
        self.exportAsPNGButton.setFixedHeight(button_height)
        self.exportAsSVGButton.setFixedHeight(button_height)
        self.updatePositionButton.setFixedHeight(button_height)
        self.selectAllButton.setFixedHeight(button_height)
        add_to_sequence_button.setFixedHeight(button_height)

        self.deleteButton.setIconSize(icon_size)
        self.rotateRightButton.setIconSize(icon_size)
        self.rotateLeftButton.setIconSize(icon_size)
        self.mirrorButton.setIconSize(icon_size)
        self.bringForward.setIconSize(icon_size)
        self.swapColors.setIconSize(icon_size)
        self.exportAsPNGButton.setIconSize(icon_size)
        self.exportAsSVGButton.setIconSize(icon_size)
        self.updatePositionButton.setIconSize(icon_size)
        self.selectAllButton.setIconSize(icon_size)
        add_to_sequence_button.setIconSize(icon_size)
        
        buttonstack.addWidget(self.deleteButton)
        buttonstack.addWidget(self.rotateRightButton)
        buttonstack.addWidget(self.rotateLeftButton)
        buttonstack.addWidget(self.mirrorButton)
        buttonstack.addWidget(self.bringForward)
        buttonstack.addWidget(self.swapColors)
        buttonstack.addWidget(self.exportAsPNGButton)
        buttonstack.addWidget(self.exportAsSVGButton)
        buttonstack.addWidget(self.updatePositionButton)
        buttonstack.addWidget(self.selectAllButton)
        buttonstack.addWidget(add_to_sequence_button)


        self.button_layout.addLayout(masterbtnlayout)

    def initArrowBox(self):
        arrowbox_frame = QFrame(self.main_window)
        objectbox_layout = QGridLayout()  # Change this to QGridLayout
        arrowbox_frame.setLayout(objectbox_layout)  # set the layout to the frame

        arrowbox_scene = QGraphicsScene()

        for arrow in self.arrows:
            arrowbox_scene.addItem(arrow)  # use arrowbox_scene here
            arrow.attributesChanged.connect(self.info_tracker.update)
            arrow.attributesChanged.connect(lambda: self.generator.update_staff(arrow, self.staff_manager))

        svgs_full_paths = []
        default_arrows = ['red_iso_r_ne.svg', 'red_anti_r_ne.svg', 'blue_iso_r_sw.svg', 'blue_anti_r_sw.svg']
        svg_item_count = 0

        for dirpath, dirnames, filenames in os.walk(self.ARROW_DIR):
            svgs_full_paths.extend([os.path.join(dirpath, filename) for filename in filenames if filename.endswith('.svg')])

        svg_item_count_red_iso = 0
        svg_item_count_red_anti = 0
        svg_item_count_blue_iso = 0
        svg_item_count_blue_anti = 0
        spacing = 200  # Define the spacing between items
        y_pos_red = 0  # y position for red arrows
        y_pos_blue = 200  # y position for blue arrows

        for i, svg_file in enumerate(svgs_full_paths):
            file_name = os.path.basename(svg_file)
            if file_name in default_arrows:
                self.graphboard.set_handlers(self.arrow_handler)
                arrow_item = Arrow(svg_file, self.graphboard, self.info_tracker, self.svg_handler, self.arrow_handler)
                arrow_item.setFlag(QGraphicsItem.ItemIsMovable, True)
                arrow_item.setFlag(QGraphicsItem.ItemIsSelectable, True)
                arrow_item.setScale(0.75)

                if 'red' in file_name:
                    if 'iso' in file_name:
                        arrow_item.setPos(svg_item_count_red_iso * spacing, y_pos_red)  # Set the position of the red iso item
                        svg_item_count_red_iso += 1
                    elif 'anti' in file_name:
                        arrow_item.setPos((svg_item_count_red_anti + 1) * spacing, y_pos_red)  # Set the position of the red anti item
                        svg_item_count_red_anti += 1
                elif 'blue' in file_name:
                    if 'iso' in file_name:
                        arrow_item.setPos(svg_item_count_blue_iso * spacing, y_pos_blue)  # Set the position of the blue iso item
                        svg_item_count_blue_iso += 1
                    elif 'anti' in file_name:
                        arrow_item.setPos((svg_item_count_blue_anti + 1) * spacing, y_pos_blue)  # Set the position of the blue anti item
                        svg_item_count_blue_anti += 1

                arrowbox_scene.addItem(arrow_item) 
                print(self.info_tracker)
                arrow_item.attributesChanged.connect(self.info_tracker.update)

                self.arrows.append(arrow_item)


        arrowbox = Arrow_Box(arrowbox_scene, self.graphboard, self.info_tracker, self.svg_handler)

        objectbox_layout.addWidget(arrowbox) 
        arrowbox_frame.setFixedSize(500, 500)
        self.objectbox_layout.addWidget(arrowbox_frame)  # Add arrowbox_frame to upper_layout

    def initPropBox(self):
        self.propbox = Prop_Box(self.main_window, self.staff_manager, self)
        propbox_layout = QVBoxLayout()  # Create a new QVBoxLayout
        propbox_layout.addWidget(self.propbox.prop_box_frame)  # Add the QFrame object to the layout
        propbox_frame = QFrame()  # Create a new QFrame
        propbox_frame.setLayout(propbox_layout)  # Set the layout to the frame
        self.objectbox_layout.addWidget(propbox_frame)  # Add the frame to the upper_layout

    def initInfoTracker(self):
        self.info_label = QLabel(self.main_window)
        self.info_tracker = Info_Tracker(None, self.info_label, self, self.staff_manager)

    def initWordLabel(self):
        self.word_label = QLabel(self.main_window)
        self.lower_layout.addWidget(self.word_label)
        self.word_label.setFont(QFont('Helvetica', 20))
        self.word_label.setText("My word: ")

    def initSequenceScene(self):
        self.sequence_scene = Sequence_Scene()  # Create a new Sequence_Scene instance
        self.sequence_manager = Sequence_Manager(self.sequence_scene, self.generator, self, self.info_tracker)

        self.sequence_scene.set_manager(self.sequence_manager)  # Set the manager of the sequence container
        self.sequence_manager.manager = self.sequence_manager  # Set the manager of the sequence scene

        self.sequence_container = QGraphicsView(self.sequence_scene)  # Create a QGraphicsView with the sequence scene

        # Set the width and height
        self.sequence_container.setFixedSize(1960, 500)
        self.sequence_container.show()
        self.lower_layout.addWidget(self.sequence_container)

        clear_sequence_button = self.sequence_manager.get_clear_sequence_button()
        self.lower_layout.addWidget(clear_sequence_button)


    def initGenerator(self):
        self.generator = Pictograph_Generator(self.staff_manager, self.graphboard, self.graphboard, self.graphboard_scene, self.info_tracker, self.handlers, self.main_window, self, self.arrow_handler)

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
        self.key_press_handler.handleKeyPressEvent(event)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            self.keyPressEvent(event)
            return True
        return super().eventFilter(source, event)