from typing import TYPE_CHECKING
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy
from widgets.graph_editor_tab.graph_editor_attr_panel import GraphEditorAttrPanel
from widgets.graph_editor_tab.graph_editor_pictograph import GraphEditorPictograph, GraphEditorPictographView


from widgets.graph_editor_tab.graph_editor_pictograph_widget import (
    GraphEditorPictographWidget,
)

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class GraphEditor(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window

        self._setup_graph_editor_pictograph(main_widget)

        self.pictograph_widget = GraphEditorPictographWidget(
            self, self.graph_editor_pictograph.view
        )
        self._setup_main_layout()

    def _setup_graph_editor_pictograph(self, main_widget):
        self.graph_editor_pictograph = GraphEditorPictograph(main_widget, self)
        self.graph_editor_pictograph_view = GraphEditorPictographView(self)
        self.graph_editor_pictograph_view.setScene(self.graph_editor_pictograph)

    def _setup_frame_style(self) -> None:
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.setPalette(palette)

    def _setup_main_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.pictograph_layout = QVBoxLayout()
        self.pictograph_layout.addWidget(self.pictograph_widget)
        self.layout.addLayout(self.pictograph_layout)
        self.layout.setAlignment(self.main_widget, Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)

