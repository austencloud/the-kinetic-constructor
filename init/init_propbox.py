from views.propbox_view import PropBox_View
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt
from settings import GRAPHBOARD_SCALE


class Init_PropBox():
    def __init__(self, ui_setup, main_window, staff_manager):
        self.init_propbox_view(ui_setup, main_window, staff_manager)
    
    def init_propbox_view(self, ui_setup, main_window, staff_manager):
        propbox_scene = QGraphicsScene()
        propbox_view = PropBox_View(main_window, staff_manager, ui_setup)
        propbox_frame = QFrame(main_window)
        propbox_view.setScene(propbox_scene)
        propbox_layout = QVBoxLayout()
        propbox_frame.setLayout(propbox_layout)

        propbox_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        propbox_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        propbox_view.setFrameShape(QFrame.NoFrame)

        propbox_layout.addWidget(propbox_view)
        propbox_frame.setFixedSize(int(500 * GRAPHBOARD_SCALE), int(400 * GRAPHBOARD_SCALE))
        main_window.objectbox_layout.addWidget(propbox_frame)

        ui_setup.propbox_view = propbox_view
        ui_setup.propbox_scene = propbox_scene
        