from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QFrame, QVBoxLayout
from staff import PropBox_Staff
from PyQt5.QtCore import Qt
class PropBox_Scene(QGraphicsScene):
    def __init__(self, main_window, staff_manager, ui_setup):
        super().__init__()
        self.main_window = main_window
        self.staff_manager = staff_manager
        self.ui_setup = ui_setup
        self.propbox_frame = self.init_propbox_frame()

    def init_propbox_frame(self):
        propbox_frame = QFrame(self.main_window)


        propbox_view = QGraphicsView(self)
        propbox_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        propbox_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        propbox_view.setFrameShape(QFrame.NoFrame)
        layout = QVBoxLayout()  # Create a new QVBoxLayout
        layout.addWidget(propbox_view)  # Add the view to the layout
        
        propbox_frame.setLayout(layout)  # Set the layout to the propbox
        propbox_frame.setFixedSize(500, 500)

        return propbox_frame  # Return the QFrame object
