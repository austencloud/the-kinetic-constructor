from PyQt5.QtWidgets import QGraphicsScene, QScrollArea, QGraphicsView, QFrame, QVBoxLayout
from staff import PropBox_Staff

class Prop_Box:
    def __init__(self, main_window, staff_manager, ui_setup):
        self.main_window = main_window
        self.staff_manager = staff_manager
        self.ui_setup = ui_setup
        self.prop_box_frame = self.initPropBox()

    def initPropBox(self):
        propbox = QFrame(self.main_window)
        propbox_scene = QGraphicsScene()
        self.staff_manager.init_staves(propbox_scene)

        # Create staff objects and add them to the scene
        self.red_staff = PropBox_Staff('red_staff', propbox_scene, self.staff_manager.staff_locations['N_staff'], 'red', 'images\\staves\\N_staff_red.svg')
        self.blue_staff = PropBox_Staff('blue_staff', propbox_scene, self.staff_manager.staff_locations['N_staff'], 'blue', 'images\\staves\\N_staff_blue.svg')

        # propbox_scene.addItem(self.red_staff)
        # propbox_scene.addItem(self.blue_staff)

        #set locations of the items to show in the propbox's center
        self.red_staff.setPos(100, 100)
        
        view = QGraphicsView(propbox_scene)
        view.setFrameShape(QFrame.NoFrame)

        layout = QVBoxLayout()  # Create a new QVBoxLayout
        layout.addWidget(view)  # Add the view to the layout
        propbox.setLayout(layout)  # Set the layout to the propbox

        propbox.setFixedSize(500, 500)

        return propbox  # Return the QFrame object
