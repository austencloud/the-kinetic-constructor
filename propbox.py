from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt

class PropBox_View(QGraphicsView):
    def __init__(self, main_window, staff_manager, ui_setup):
        super().__init__()
        self.main_window = main_window
        self.staff_manager = staff_manager
        self.ui_setup = ui_setup
        self.propbox_scene = QGraphicsScene()
        self.setScene(self.propbox_scene)
        self.propbox_frame = self.init_propbox_frame()

    def init_propbox_frame(self):
        propbox_frame = QFrame(self.main_window)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        layout = QVBoxLayout()
        layout.addWidget(self)
        
        propbox_frame.setLayout(layout)
        propbox_frame.setFixedSize(500, 500)

        return propbox_frame
