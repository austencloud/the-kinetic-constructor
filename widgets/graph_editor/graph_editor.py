from typing import TYPE_CHECKING

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy

from widgets.graph_editor.object_panel.arrowbox.arrowbox import ArrowBox
from widgets.graph_editor.pictograph.pictograph import Pictograph
from widgets.graph_editor.object_panel.propbox.propbox import PropBox
from widgets.graph_editor.attr_panel.attr_panel import AttrPanel
from widgets.graph_editor.pictograph.pictograph import Pictograph


if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class GraphEditor(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.json_handler = main_widget.json_handler
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.setPalette(palette)

        graph_editor_frame_layout = QHBoxLayout(self)
        graph_editor_frame_layout.setSpacing(0)
        graph_editor_frame_layout.setContentsMargins(0, 0, 0, 0)
        graph_editor_frame_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        objectbox_layout = QVBoxLayout()
        pictograph_layout = QVBoxLayout()

        self.pictograph = Pictograph(self.main_widget, self)

        self.arrowbox = ArrowBox(main_widget, self)
        self.propbox = PropBox(main_widget, self)
        self.attr_panel = AttrPanel(self.pictograph)

        objectbox_layout.addWidget(self.arrowbox.view)
        objectbox_layout.addWidget(self.propbox.view)
        pictograph_layout.addWidget(self.pictograph.view)

        graph_editor_frame_layout.setContentsMargins(0, 0, 0, 0)
        graph_editor_frame_layout.addLayout(objectbox_layout)
        graph_editor_frame_layout.addLayout(pictograph_layout)
        graph_editor_frame_layout.addWidget(self.attr_panel)

        self.setLayout(graph_editor_frame_layout)
        self.setMouseTracking(True)

