from PyQt6.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout
from widgets.graphboard.graphboard import GraphBoard
from widgets.arrowbox.arrowbox import Arrowbox
from widgets.propbox.propbox import Propbox
from widgets.infobox.infobox import InfoBox
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtGui import QPalette, QColor
from widgets.action_buttons_frame import ActionButtonsFrame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class GraphEditor(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.json_handler = main_widget.json_handler

        self.graph_editor_frame = QFrame()
        self.graph_editor_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.graph_editor_frame.setLineWidth(1)
        palette = self.graph_editor_frame.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.graph_editor_frame.setPalette(palette)

        graph_editor_frame_layout = QHBoxLayout(self.graph_editor_frame)

        objectbox_layout = QVBoxLayout()
        graphboard_layout = QVBoxLayout()
        action_buttons_layout = QVBoxLayout()
        infobox_layout = QVBoxLayout()

        self.graphboard = GraphBoard(self.main_widget)
        self.infobox = InfoBox(
            main_widget,
            self.graphboard,
        )
        self.graphboard.infobox = self.infobox
        self.propbox = Propbox(main_widget)
        self.arrowbox = Arrowbox(
            main_widget,
            self.infobox,
        )
        self.action_buttons_frame = ActionButtonsFrame(
            self.graphboard,
            self.json_handler,
        )

        objectbox_layout.addWidget(self.arrowbox.view)
        objectbox_layout.addWidget(self.propbox.view)
        graphboard_layout.addWidget(self.graphboard.view)
        action_buttons_layout.addWidget(self.action_buttons_frame)
        infobox_layout.addWidget(self.infobox)

        graph_editor_frame_layout.addLayout(objectbox_layout)
        graph_editor_frame_layout.addLayout(graphboard_layout)
        graph_editor_frame_layout.addLayout(action_buttons_layout)
        graph_editor_frame_layout.addLayout(infobox_layout)

        self.graph_editor_frame.setLayout(graph_editor_frame_layout)
        self.main_window.graph_editor_layout.addWidget(self.graph_editor_frame)

        self.setMouseTracking(True)
