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

        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.setPalette(palette)

        # Set up the main layout for the GraphEditor
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set up child layouts
        self.objectbox_layout = QVBoxLayout()
        self.pictograph_layout = QVBoxLayout()
        self.attr_panel_layout = QVBoxLayout()

        self.pictograph = Pictograph(self.main_widget, self)
        self.arrowbox = ArrowBox(main_widget, self)
        self.propbox = PropBox(main_widget, self)
        self.attr_panel = AttrPanel(self)

        # Add child widgets to their respective layouts
        self.objectbox_layout.addWidget(self.arrowbox.view)
        self.objectbox_layout.addWidget(self.propbox.view)
        self.pictograph_layout.addWidget(self.pictograph.view)
        self.attr_panel_layout.addWidget(self.attr_panel)

        # Add child layouts to the main layout
        self.layout.addLayout(self.objectbox_layout)
        self.layout.addLayout(self.pictograph_layout)
        self.layout.addLayout(self.attr_panel_layout)

        # Apply the layout to the GraphEditor
        self.setLayout(self.layout)

        # Ensure that the GraphEditor can resize freely in both directions
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.pictograph.view.fitInView(
            self.pictograph.view.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio
        )
        self.arrowbox.view.setMinimumWidth(int(self.pictograph.view.height() / 2))
        self.arrowbox.view.fitInView(
            self.arrowbox.view.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio
        )
        self.propbox.view.setMinimumWidth(int(self.pictograph.view.height() / 2))
        self.propbox.view.fitInView(
            self.propbox.view.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio
        )
        self.set_height_to_attr_panel_widgets_height() 

    def set_height_to_attr_panel_widgets_height(self):
        required_height = sum(
            widget.sizeHint().height()
            for widget in self.attr_panel.red_attr_box.widgets
        )
        self.setMinimumHeight(required_height)
