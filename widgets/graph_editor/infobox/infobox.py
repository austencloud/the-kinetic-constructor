from PyQt6.QtWidgets import QFrame, QHBoxLayout
from widgets.graph_editor.infobox.control_panel.control_panel import ControlPanel
from widgets.graph_editor.infobox.info_panel import InfoPanel
from widgets.graph_editor.graphboard.graphboard import GraphBoard
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget

class InfoBox(QFrame):
    """
    The InfoBox widget displays information related to the graph editor.

    Args:
        main_widget (MainWidget): The main widget of the application.
        graphboard (GraphBoard): The graph board widget.

    Attributes:
        main_window (MainWindow): The main window of the application.
        control_panel (ControlPanel): The control panel widget.

    """
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
        self.info_panel = InfoPanel(self, graphboard)
        self.control_panel = ControlPanel(self, graphboard)
    
        self.infobox_layout = QHBoxLayout()
        self.infobox_layout.setSpacing(0)
        self.infobox_layout.setContentsMargins(0, 0, 0, 0)
        self.infobox_layout.addWidget(self.info_panel)
        self.infobox_layout.addWidget(self.control_panel)
        
        self.setLayout(self.infobox_layout)
        