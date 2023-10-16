from views.propbox_view import PropBox_View
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QGraphicsView, QGraphicsScene



class Init_PropBox():
    def __init__(self, ui_setup, main_window, staff_manager):
        self.initPropBoxView(ui_setup, main_window, staff_manager)
    
    def initPropBoxView(self, ui_setup, main_window, staff_manager):
        ui_setup.propbox_view = PropBox_View(main_window, staff_manager, ui_setup)
        propbox_layout = QVBoxLayout()
        propbox_frame = QFrame() 
        propbox_layout.addWidget(ui_setup.propbox_view.propbox_frame)
        propbox_frame.setLayout(propbox_layout)
        ui_setup.main_window.objectbox_layout.addWidget(propbox_frame)
        ui_setup.propbox_scene = QGraphicsScene()
        ui_setup.propbox_view.setScene(ui_setup.propbox_scene)