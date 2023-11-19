from typing import TYPE_CHECKING

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout

from widgets.graph_editor.action_buttons_frame import ActionButtonsFrame
from widgets.graph_editor.arrowbox.arrowbox import ArrowBox
from widgets.graph_editor.graphboard.graphboard import GraphBoard
from widgets.graph_editor.infobox.infobox import InfoBox
from widgets.graph_editor.propbox.propbox import PropBox

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize


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

        graph_editor_frame_layout = QHBoxLayout(self)
        graph_editor_frame_layout.setSpacing(0)
        graph_editor_frame_layout.setContentsMargins(0, 0, 0, 0)

        objectbox_layout = QVBoxLayout()
        graphboard_layout = QVBoxLayout()
        action_buttons_layout = QVBoxLayout()
        infobox_layout = QVBoxLayout()

        self.graphboard = GraphBoard(
            self.main_widget,
            self,
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

        objectbox_layout.addWidget(self.arrowbox.view)
        objectbox_layout.addWidget(self.propbox.view)

        graphboard_layout.addWidget(self.graphboard.view)
        infobox_layout.addWidget(self.infobox)

        graph_editor_frame_layout.setContentsMargins(0, 0, 0, 0)

        graph_editor_frame_layout.addLayout(objectbox_layout)
        graph_editor_frame_layout.addLayout(graphboard_layout)
        graph_editor_frame_layout.addLayout(infobox_layout)

        self.setLayout(graph_editor_frame_layout)

        self.setMouseTracking(True)

    def update_size(self) -> None:
        self.setFixedHeight(int(self.main_widget.height() * 1 / 4))
        self.setFixedWidth(int(self.main_widget.width() * 0.5))
        self.update_graphboard_size()
        self.update_arrowbox_size()
        self.update_propbox_size()

    def update_graphboard_size(self) -> None:
        view_width = int(self.height() * 75 / 90)
        self.graphboard.view.setFixedWidth(view_width)
        self.graphboard.view.setFixedHeight(self.height())
        view_scale = view_width / self.graphboard.width()
        self.graphboard.view.resetTransform()  # Reset the current transform
        self.graphboard.view.scale(view_scale, view_scale)  # Set the new scale

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
