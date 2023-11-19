from PyQt6.QtWidgets import QFrame
from widgets.graph_editor.infobox.control_panel.control_panel import ControlPanel
from widgets.graph_editor.graphboard.graphboard import GraphBoard
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget

class InfoBox(QFrame):
    def __init__(self, main_widget: "MainWidget", graphboard: "GraphBoard") -> None:
        """
        Initialize the InfoBox widget.

        Args:
            main_widget (MainWidget): The main widget of the application.
            graphboard (GraphBoard): The graph board widget.

        Returns:
            None
        """
        super().__init__()
        self.main_widget = main_widget
        self.main_window = self.main_widget.main_window
        self.graphboard = graphboard
        self.control_panel = ControlPanel(self, graphboard)

