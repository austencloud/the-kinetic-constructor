from typing import TYPE_CHECKING

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget

from widgets.action_buttons_frame import ActionButtonsFrame
from widgets.arrowbox.arrowbox import ArrowBox
from widgets.graphboard.graphboard import GraphBoard
from widgets.infobox.infobox import InfoBox
from widgets.propbox.propbox import PropBox

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class GraphEditor(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.json_handler = main_widget.json_handler

        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.setPalette(palette)

        graph_editor_frame_layout = QHBoxLayout(self)

        objectbox_layout = QVBoxLayout()
        graphboard_layout = QVBoxLayout()
        action_buttons_layout = QVBoxLayout()
        infobox_layout = QVBoxLayout()

        self.graphboard = GraphBoard(
            self.main_widget,
        )
        self.infobox = InfoBox(
            main_widget,
            self.graphboard,
        )
        self.graphboard.infobox = self.infobox
        self.propbox = PropBox(main_widget)
        self.arrowbox = ArrowBox(
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
        self.graph_editor_frame_layout = graph_editor_frame_layout
        self.setLayout(graph_editor_frame_layout)
        
        self.setMouseTracking(True)

