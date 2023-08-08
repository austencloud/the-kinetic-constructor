from PyQt5.QtWidgets import QAction, QApplication, QHBoxLayout, QVBoxLayout, QScrollArea, QGraphicsScene, QGraphicsView, QGraphicsItem, QLabel, QFrame, QWidget, QLineEdit, QGridLayout
import os
from arrow import Arrow
from PyQt5.QtGui import QFont, QTransform, QIcon, QPixmap
from sequence import *
from info_tracker import Info_Tracker
from generator import Pictograph_Generator
from staff import *
from letter import Letter_Manager
from PyQt5.QtCore import Qt, QPointF, QEvent, QSize
from handlers import Arrow_Handler, Svg_Handler, Json_Handler 
from arrowbox import Arrow_Box
from propbox import Prop_Box
from menus import Menu_Bar, Context_Menu_Handler
from graphboard import Graphboard
from exporter import Exporter

class UiSetup(QWidget):
    resolution_4k = pyqtSignal()
    resolution_2400x1600 = pyqtSignal()
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setFocusPolicy(Qt.StrongFocus)
        self.main_window = main_window
        self.main_window.installEventFilter(self)

        self.main_window.setWindowTitle("Sequence Generator")
        self.main_window.show()
        
        self.svg_handler = Svg_Handler()
        self.graphboard_scene = QGraphicsScene()
        self.menu_bar = Menu_Bar(self.main_window)
        
        self.arrows = []
        self.ARROW_DIR = 'images\\arrows'
        self.SVG_POS_Y = 250
        
        self.context_menu_handler = None
        self.exporter = None
        self.ui_setup = self
        self.sequence_handler = None
        self.graphboard = None
        self.arrow_handler = None

        self.main_container = QWidget()
        self.main_container.setMinimumSize(2000, 1500)

        # Set the main container as the central widget of the main window
        self.main_window.setCentralWidget(self.main_container)
        self.get_screen_resolution()
        self.initMenuBars()
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

    def initMenuBars(self):
        file_menu = self.menu_bar.addMenu('File')
        refresh_action = QAction('Refresh UI', self.main_window)
        refresh_action.triggered.connect(self.main_window.refresh_ui)  # Assuming you have a method called refresh_ui
        file_menu.addAction(refresh_action)
        self.main_window.setMenuBar(self.menu_bar)
        
    def initMenus(self):
        self.json_updater = Json_Handler(self.graphboard_scene)
        self.context_menu_handler = Context_Menu_Handler(self.graphboard_scene, self.sequence_handler, self.arrow_handler, self.exporter)
        self.arrow_handler = Arrow_Handler(self.graphboard_scene, self.graphboard, self.staff_manager)


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
        self.main_container.setLayout(self.main_layout)


    def initGraphboard(self):
        self.grid = Grid('images\\grid\\grid.svg', self.ui_setup)
        # Initialize graphboard without generator
        self.graphboard = Graphboard(self.graphboard_scene, self.grid, self.info_tracker, self.staff_manager, self.svg_handler, self, None, self.sequence_handler)
        self.exporter = Exporter(self.graphboard, self.graphboard_scene, self.staff_manager, self.grid)

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
            ['W', 'X', 'Y', 'Z'],
            ['Σ', 'Δ', 'θ', 'Ω'],
            # ['Φ', 'Ψ', 'Λ'],
            # ['W-', 'X-', 'Y-', 'Z-'],
            # ['Σ-', 'Δ-', 'θ-', 'Ω-'],
            # ['Φ-', 'Ψ-', 'Λ-'],
            # ['α', 'β', 'Γ']
        ]
        # Iterate through the letter rows and create buttons with icons
        for row in letter_rows:
            row_layout = QHBoxLayout()  # Create a new horizontal layout for the row
            for letter in row:
                icon_path = f"images/letters/{letter}.svg"
                renderer = QSvgRenderer(icon_path)  # Create a renderer for the SVG file

                # Create a QPixmap to render the SVG into
                pixmap = QPixmap(renderer.defaultSize())
                pixmap.fill(Qt.transparent)

                # Render the SVG into the QPixmap
                painter = QPainter(pixmap)
                renderer.render(painter)
                painter.end()

                button = QPushButton(QIcon(pixmap), "", self.main_window)  # Create a new button
                font = QFont()
                font.setPointSize(20)
                button.setFont(font)
                button.setFixedSize(65, 65)
                button.clicked.connect(lambda _, l=letter: self.generator.generate_pictograph(l, self.staff_manager))  # use self.generator here
                row_layout.addWidget(button)  # Add the button to the row layout
            letter_buttons_layout.addLayout(row_layout)  # Add the row layout to the main layout

        # Add a button to generate all letters
        generate_all_button = QPushButton("Generate All", self.main_window)
        font = QFont()
        font.setPointSize(20)
        generate_all_button.setFont(font)
        generate_all_button.setFixedSize(300, 80)
        generate_all_button.clicked.connect(lambda: self.generator.generate_all_pictographs(self.staff_manager))  # replace "/path/to/output/directory" with your desired output directory
        letter_buttons_layout.addWidget(generate_all_button)

        self.upper_layout.addLayout(letter_buttons_layout)  # add the layout to left_layout here

    def initButtons(self):
        button_font = QFont('Helvetica', 14)
        button_width = 60
        button_height = 60
        icon_size = QSize(40, 40)

        masterbtnlayout = QVBoxLayout()
        buttonlayout = QHBoxLayout()
        buttonstack = QHBoxLayout()
        buttonstack.setAlignment(Qt.AlignTop)
        masterbtnlayout.setAlignment(Qt.AlignTop)
        buttonlayout.addLayout(buttonstack)
        masterbtnlayout.addLayout(buttonlayout)

        def createButton(icon_path, tooltip, on_click, is_lambda=False):
            button = QPushButton(QIcon(icon_path), "")
            button.setToolTip(tooltip)
            button.setFont(button_font)
            button.setFixedWidth(button_width)
            button.setFixedHeight(button_height)
            button.setIconSize(icon_size)
            if is_lambda:
                button.clicked.connect(lambda: on_click())
            else:
                button.clicked.connect(on_click)
            return button

        self.updatePositionButton = createButton("images/icons/update_locations.png", "Update Position", 
            lambda: self.json_updater.updatePositionInJson(*self.graphboard.get_current_arrow_positions()), is_lambda=True)
        self.deleteButton = createButton("images/icons/delete.png", "Delete",
            lambda: self.arrow_handler.delete_arrow(self.graphboard_scene.selectedItems()), is_lambda=True)
        self.rotateRightButton = createButton("images/icons/rotate_right.png", "Rotate Right",
            lambda: self.arrow_handler.rotate_arrow('right', self.graphboard_scene.selectedItems()), is_lambda=True)        
        self.rotateLeftButton = createButton("images/icons/rotate_left.png", "Rotate Left",
            lambda: self.arrow_handler.rotate_arrow('left', self.graphboard_scene.selectedItems()), is_lambda=True)
        self.mirrorButton = createButton("images/icons/mirror.png", "Mirror",
            lambda: self.arrow_handler.mirror_arrow(self.graphboard_scene.selectedItems()), is_lambda=True)
        self.bringForward = createButton("images/icons/bring_forward.png", "Bring Forward",
            lambda: self.arrow_handler.bring_forward(self.graphboard_scene.selectedItems()), is_lambda=True)
        self.swapColors = createButton("images/icons/swap.png", "Swap Colors",
            lambda: self.arrow_handler.swap_colors(self.graphboard_scene.selectedItems()), is_lambda=True)
        self.export_to_png_button = createButton("images/icons/export.png", "Export to PNG",
            lambda: self.exporter.export_to_png(), is_lambda=True)
        self.export_to_svg_button = createButton("images/icons/export.png", "Export to SVG",
            lambda: self.exporter.export_to_svg('output.svg'), is_lambda=True)
        self.selectAllButton = createButton("images/icons/select_all.png", "Select All",
            lambda: self.graphboard.select_all_arrows(), is_lambda=True)
        self.add_to_sequence_button = createButton("images/icons/add_to_sequence.png", "Add to Sequence",
            lambda: self.sequence_handler.add_to_sequence(self.graphboard), is_lambda=True)
        
        buttons = [
            self.deleteButton, 
            self.rotateRightButton,
            self.rotateLeftButton,
            self.mirrorButton,
            self.bringForward,
            self.swapColors,
            self.export_to_png_button,
            self.export_to_svg_button,
            self.updatePositionButton,
            self.selectAllButton,
            self.add_to_sequence_button
        ]

        for button in buttons:
            buttonstack.addWidget(button)

        self.button_layout.addLayout(masterbtnlayout)

    def initArrowBox(self):
        arrowbox_frame = QFrame(self.main_window)
        objectbox_layout = QGridLayout()  # Change this to QGridLayout
        arrowbox_frame.setLayout(objectbox_layout)  # set the layout to the frame

        arrowbox_scene = QGraphicsScene()

        for arrow in self.arrows:
            arrowbox_scene.addItem(arrow)  # use arrowbox_scene here

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
                arrow_item = Arrow(svg_file, self.graphboard, self.info_tracker, self.svg_handler, self.arrow_handler, self.ui_setup)
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
        self.sequence_handler = Sequence_Handler(self.sequence_scene, self.generator, self, self.info_tracker)

        self.sequence_scene.set_manager(self.sequence_handler)  # Set the manager of the sequence container
        self.sequence_handler.manager = self.sequence_handler  # Set the manager of the sequence scene

        self.sequence_container = QGraphicsView(self.sequence_scene)  # Create a QGraphicsView with the sequence scene

        # Set the width and height
        self.sequence_container.setFixedSize(1960, 300)
        #disable scrollbars
        self.sequence_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sequence_container.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sequence_container.show()
        self.lower_layout.addWidget(self.sequence_container)

        clear_sequence_button = self.sequence_handler.get_clear_sequence_button()
        self.lower_layout.addWidget(clear_sequence_button)


    def initGenerator(self):
        self.generator = Pictograph_Generator(self.staff_manager, self.graphboard, self.graphboard_scene, self.info_tracker, self.main_window, self, self.exporter, self.context_menu_handler, self.grid, self)

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

    def connectGraphboard(self):
        self.info_tracker.set_graphboard(self.graphboard)
        self.graphboard_layout.addWidget(self.graphboard)


### GETTERS ###

    def get_sequence_manager(self):
        if not hasattr(self, 'sequence_handler'):
            self.sequence_handler = Sequence_Handler(self.sequence_scene, self.generator, self, self.info_tracker)
            self.sequence_scene.set_manager(self.sequence_handler)  # Set the manager of the sequence container
            self.sequence_handler.manager = self.sequence_handler  # Set the manager of the sequence scene
        return self.sequence_handler

    def get_screen_resolution(self):
        screen_resolution = QApplication.desktop().screenGeometry()
        screen_width, screen_height = screen_resolution.width(), screen_resolution.height()

        if screen_width == 3840 and screen_height == 2160:
            self.resolution_4k.emit()
            print("4k detected")
        elif screen_width == 2400 and screen_height == 1600:
            self.resolution_2400x1600.emit()
            print("2400x1600 detected")

### EVENTS ###

    def keyPressEvent(self, event):
        self.selected_items = self.graphboard.get_selected_items()
        self.arrow = self.selected_items[0]

        if event.key() == Qt.Key_Delete:

            self.arrow_handler.delete_arrow(self.selected_items)

        print(self.selected_items) 
        if event.key() == Qt.Key_W:
            self.arrow.move_quadrant_up()
            print("W")
        elif event.key() == Qt.Key_A:
            self.arrow.move_quadrant_left()
        elif event.key() == Qt.Key_S:
            self.arrow.move_quadrant_down()
        elif event.key() == Qt.Key_D:
            self.arrow.move_quadrant_right()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            self.keyPressEvent(event)
            return True
        return super().eventFilter(source, event)