from typing import TYPE_CHECKING

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout

from widgets.graph_editor.arrowbox.arrowbox import ArrowBox
from widgets.graph_editor.graphboard.graphboard import GraphBoard
from widgets.graph_editor.propbox.propbox import PropBox
from widgets.graph_editor.attr_panel.attr_panel import AttrPanel
from widgets.graph_editor.vtg_panel import VTGPanel
from widgets.graph_editor.graphboard.graphboard import GraphBoard


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
        # remove the space in between each widget in the frame
        self.setFixedHeight(int(self.main_widget.height() * 1 / 4))
        self.setFixedWidth(int(self.main_widget.width() * 0.5))

        graph_editor_frame_layout = QHBoxLayout(self)
        graph_editor_frame_layout.setSpacing(0)
        graph_editor_frame_layout.setContentsMargins(0, 0, 0, 0)

        objectbox_layout = QVBoxLayout()
        graphboard_layout = QVBoxLayout()
        attr_panel_layout = QVBoxLayout()
        vtg_panel_layout = QVBoxLayout()

        self.graphboard = GraphBoard(self.main_widget, self)
        self.propbox = PropBox(main_widget, self.graphboard)
        self.arrowbox = ArrowBox(main_widget)
        self.vtg_panel = VTGPanel(self.graphboard)
        self.attr_panel = AttrPanel(self.graphboard)

        objectbox_layout.addWidget(self.arrowbox.view)
        objectbox_layout.addWidget(self.propbox.view)
        graphboard_layout.addWidget(self.graphboard.view)
        attr_panel_layout.addWidget(self.attr_panel)
        vtg_panel_layout.addWidget(self.vtg_panel)

        graph_editor_frame_layout.setContentsMargins(0, 0, 0, 0)
        graph_editor_frame_layout.addLayout(objectbox_layout)
        graph_editor_frame_layout.addLayout(graphboard_layout)
        graph_editor_frame_layout.addLayout(attr_panel_layout)
        graph_editor_frame_layout.addLayout(vtg_panel_layout)

        self.setLayout(graph_editor_frame_layout)
        self.setMouseTracking(True)

    def update_size(self) -> None:
        self.setFixedHeight(int(self.main_widget.height() * 1 / 3))
        self.setFixedWidth(int(self.main_widget.width() * 0.5))
        self.graphboard.update_graphboard_size()
        self.update_arrowbox_size()
        self.update_propbox_size()
        self.update_attr_panel_size()
        self.update_vtg_panel_size()



    def update_arrowbox_size(self) -> None:
        self.arrowbox.view.setFixedSize(
            int(self.graphboard.view.height() * 1 / 2),
            int(self.graphboard.view.height() * 1 / 2),
        )

    def update_propbox_size(self) -> None:
        self.propbox.view.setFixedSize(
            int(self.graphboard.view.height() * 1 / 2),
            int(self.graphboard.view.height() * 1 / 2),
        )

    def update_attr_panel_size(self) -> None:
        self.attr_panel.setFixedHeight(self.height())
        self.attr_panel.setFixedWidth(int(self.height() / 2))
        self.attr_panel.red_attr_box.update_attr_box_size()
        self.attr_panel.blue_attr_box.update_attr_box_size()

    def update_vtg_panel_size(self) -> None:
        self.vtg_panel.setFixedHeight(self.height())
        self.vtg_panel.setFixedWidth(int(self.width() / 2))
