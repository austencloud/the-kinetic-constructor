from typing import TYPE_CHECKING

from widgets.graph_editor_tab.graph_editor_frame import GraphEditorFrame

if TYPE_CHECKING:
    from widgets.main_tab_widget import MainTabWidget
    from widgets.main_widget import MainWidget
from PyQt6.QtWidgets import QFrame, QHBoxLayout
from PyQt6.QtCore import Qt


class GraphEditorTab(QFrame):
    def __init__(self, main_widget: "MainWidget", main_tab_widget: "MainTabWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.main_layout = QHBoxLayout(self)
        self.setup_ui()
        # self.add_black_borders()

    def add_black_borders(self) -> None:
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setLineWidth(1)

    def setup_ui(self) -> None:
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

        self.main_layout.setAlignment(self.main_widget, Qt.AlignmentFlag.AlignCenter)
        self.graph_editor = GraphEditorFrame(self.main_widget, self)

        self.main_layout.addWidget(self.graph_editor)
