from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QGraphicsView,
    QGraphicsScene,
)
from PyQt6.QtCore import Qt
from settings.numerical_constants import GRAPHBOARD_SCALE
from widgets.graph_editor.propbox.propbox_staff_handler import PropboxStaffHandler


class Propbox(QGraphicsScene):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget

        self.propbox_frame = QFrame()
        self.view = QGraphicsView()
        self.view.setScene(self)

        self.view.setFixedSize(int(450 * GRAPHBOARD_SCALE), int(450 * GRAPHBOARD_SCALE))
        self.setSceneRect(
            0, 0, int(450 * GRAPHBOARD_SCALE), int(450 * GRAPHBOARD_SCALE)
        )

        self.propbox_layout = QVBoxLayout()
        self.propbox_frame.setLayout(self.propbox_layout)
        self.propbox_layout.addWidget(self.view)
        self.view.setFrameStyle(QFrame.Shape.NoFrame)

        self.scale = GRAPHBOARD_SCALE * 0.75
        self.staff_handler = PropboxStaffHandler(main_widget)

        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setFrameShape(QFrame.Shape.NoFrame)

        main_widget.propbox = self
