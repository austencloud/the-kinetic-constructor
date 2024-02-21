from typing import TYPE_CHECKING
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout
from widgets.graph_editor.components.GE_turns_panel import GE_TurnsPanel
from widgets.graph_editor.components.GE_pictograph import (
    GE_BlankPictograph,
    GE_PictographView,
)


from widgets.graph_editor.components.GE_pictograph_container import (
    GE_PictographContainer,
)
from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_modifier import SequenceModifier


class GraphEditor(QFrame):
    def __init__(self, sequence_modifier: "SequenceModifier") -> None:
        super().__init__()
        self.sequence_modifier = sequence_modifier
        self.main_widget = sequence_modifier.main_widget
        self._setup_pictograph()
        self._setup_adjustment_panel()
        self._setup_layout()

    def _setup_pictograph(self):
        self.GE_pictograph = GE_BlankPictograph(self)
        self.GE_pictograph_view = GE_PictographView(self, self.GE_pictograph)
        self.GE_pictograph_container = GE_PictographContainer(
            self, self.GE_pictograph_view
        )

    def _setup_adjustment_panel(self):
        self.turns_panel = GE_TurnsPanel(self)
        self.turns_panel.setContentsMargins(0, 0, 0, 0)

    def _setup_frame_style(self) -> None:
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.setPalette(palette)

    def _setup_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.pictograph_layout = QVBoxLayout()
        self.pictograph_layout.addWidget(self.GE_pictograph_container)
        self.layout.addLayout(self.pictograph_layout)

        self.adjustment_panel_layout = QVBoxLayout()
        self.adjustment_panel_layout.addWidget(self.turns_panel)
        self.layout.addLayout(self.adjustment_panel_layout)

        self.setLayout(self.layout)

    def render_pictograph(self, pictograph: Pictograph) -> None:
        self.GE_pictograph.view.setScene(pictograph)
        self.GE_pictograph_view.pictograph = pictograph
        self.GE_pictograph = pictograph

    def resize_graph_editor(self):
        self.GE_pictograph_container.resize_GE_pictograph_container()
        self.turns_panel.resize_GE_adjustment_panel()
