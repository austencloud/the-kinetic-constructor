from PyQt6.QtWidgets import QFrame, QHBoxLayout
from widgets.graph_editor.infobox.attribute_panel.attribute_panel import AttributePanel
from widgets.graph_editor.infobox.vtg_panel import VTGPanel
from widgets.graph_editor.graphboard.graphboard import GraphBoard
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.graph_editor import GraphEditor


class InfoBox(QFrame):
    """
    The InfoBox widget displays information related to the graph editor.

    Args:
        main_widget (MainWidget): The main widget of the application.
        graphboard (GraphBoard): The graph board widget.

    Attributes:
        main_window (MainWindow): The main window of the application.
        attribute_panel (ControlPanel): The control panel widget.

    """

    def __init__(
        self,
        main_widget: "MainWidget",
        graph_editor: "GraphEditor",
        graphboard: "GraphBoard",
    ) -> None:
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
        self.graph_editor = graph_editor
        self.setFixedHeight(int(self.graph_editor.height()))
        self.setFixedWidth(int(self.graph_editor.width() / 2))
        self.vtg_panel = VTGPanel(self, graphboard)
        self.attribute_panel = AttributePanel(self, graphboard)
        self.infobox_layout = QHBoxLayout()
        self.infobox_layout.setSpacing(0)
        self.infobox_layout.setContentsMargins(0, 0, 0, 0)
        self.infobox_layout.addWidget(self.attribute_panel)
        self.infobox_layout.addWidget(self.vtg_panel)
        self.setLayout(self.infobox_layout)

    def update_infobox(self) -> None:
        """
        Updates the widgets in the info box.

        Returns:
            None
        """
        self.vtg_panel.update_info_panel()
        self.attribute_panel.update_attribute_panel()

    def update_infobox_size(self) -> None:
        pass
        self.setFixedHeight(self.graph_editor.height())
        self.vtg_panel.update_vtg_panel_size()
