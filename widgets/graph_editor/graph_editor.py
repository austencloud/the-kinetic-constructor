from typing import TYPE_CHECKING
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy
from widgets.graph_editor.graph_editor_attr_panel import GraphEditorAttrPanel
from widgets.graph_editor.graph_editor_pictograph import (
    GraphEditorPictograph,
    GraphEditorPictographView,
)


from widgets.graph_editor.graph_editor_pictograph_container import (
    GraphEditorPictographContainer,
)

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_modifier_tab_widget import SequenceModifier
    from widgets.main_widget.main_widget import MainWidget


class GraphEditor(QFrame):
    def __init__(self, sequence_modifier: "SequenceModifier") -> None:
        super().__init__()
        self.sequence_modifier = sequence_modifier
        self.main_widget = sequence_modifier.main_widget
        self._setup_graph_editor_pictograph()
        self._setup_main_layout()

    def _setup_graph_editor_pictograph(self):

        self.GE_pictograph = GraphEditorPictograph(self)
        self.GE_pictograph_view = GraphEditorPictographView(self, self.GE_pictograph)
        self.GE_pictograph_container = GraphEditorPictographContainer(
            self, self.GE_pictograph_view
        )

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
        self.pictograph_layout.addWidget(self.GE_pictograph_container)
        self.layout.addLayout(self.pictograph_layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)

    def resize_graph_editor(self):
        self.GE_pictograph_container.resize_GE_pictograph_container()
