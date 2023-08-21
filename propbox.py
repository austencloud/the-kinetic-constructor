from PyQt5.QtWidgets import QGraphicsScene, QScrollArea, QGraphicsView, QFrame, QVBoxLayout
from PyQt5.QtCore import QPointF
from staff import Staff

class Prop_Box:
    def __init__(self, main_window, staff_manager, ui_setup):
        self.main_window = main_window
        self.staff_manager = staff_manager
        self.ui_setup = ui_setup
        self.prop_box_frame = self.initPropBox()

    def initPropBox(self):
        propbox = QFrame(self.main_window)
        propbox_scene = QGraphicsScene()

        # Define the initial positions for the staff objects within the prop box
        red_staff_position = QPointF(100, 100)  # Example position for red staff
        blue_staff_position = QPointF(300, 100)  # Example position for blue staff

        # Create staff objects and add them to the scene
        self.red_staff = Staff('red_staff', propbox_scene, red_staff_position, 'red', 'images\\staves\\N_staff_red.svg')
        self.blue_staff = Staff('blue_staff', propbox_scene, blue_staff_position, 'blue', 'images\\staves\\N_staff_blue.svg')

        self.red_staff.is_in_propbox = True
        self.blue_staff.is_in_propbox = True

        #set locations of the items to show in the propbox's center
        self.red_staff.setPos(100, 100)
        
        view = QGraphicsView(propbox_scene)
        view.setFrameShape(QFrame.NoFrame)

        layout = QVBoxLayout()  # Create a new QVBoxLayout
        layout.addWidget(view)  # Add the view to the layout
        propbox.setLayout(layout)  # Set the layout to the propbox

        propbox.setFixedSize(500, 500)

        return propbox  # Return the QFrame object
