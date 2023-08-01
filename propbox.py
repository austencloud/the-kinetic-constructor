from PyQt5.QtWidgets import QGraphicsScene, QScrollArea, QGraphicsView, QFrame
from staff import PropBox_Staff

class Prop_Box:
    def __init__(self, main_window, staff_manager, ui_setup):
        self.main_window = main_window
        self.staff_manager = staff_manager
        self.ui_setup = ui_setup
        self.initPropBox()

    def initPropBox(self):
        prop_box = QScrollArea(self.main_window)
        propbox_scene = QGraphicsScene()

        # Create staff objects and add them to the scene
        self.red_staff = PropBox_Staff('red_staff', propbox_scene, self.staff_manager.staff_locations['N_staff'], 'red', 'images\\staves\\N_staff_red.svg')
        self.blue_staff = PropBox_Staff('blue_staff', propbox_scene, self.staff_manager.staff_locations['N_staff'], 'blue', 'images\\staves\\N_staff_blue.svg')

        propbox_scene.addItem(self.red_staff)
        propbox_scene.addItem(self.blue_staff)

        #set locations of the items to show in the propbox's center
        self.red_staff.setPos(100, 100)

        view = QGraphicsView(propbox_scene)
        view.setFrameShape(QFrame.NoFrame)
        prop_box.setWidget(view)
        prop_box.setWidgetResizable(True)
        prop_box.setFixedSize(400, 1200)

        self.ui_setup.left_layout.addWidget(prop_box)
