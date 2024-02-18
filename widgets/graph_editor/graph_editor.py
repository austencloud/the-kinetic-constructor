from typing import TYPE_CHECKING
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy
from widgets.graph_editor.GE_adjustment_panel import GE_AdjustmentPanel
from widgets.graph_editor.GE_pictograph import (
    GE_BlankPictograph,
    GE_PictographView,
)


from widgets.graph_editor.GE_pictograph_container import (
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

        self._setup_graph_editor_pictograph()
        self._setup_turns_panel()
        self._setup_main_layout()

    def _setup_graph_editor_pictograph(self):
        self.GE_pictograph = GE_BlankPictograph(self)
        self.GE_pictograph_view = GE_PictographView(self, self.GE_pictograph)
        self.GE_pictograph_container = GE_PictographContainer(
            self, self.GE_pictograph_view
        )

    def _setup_turns_panel(self):
        self.turns_panel = GE_AdjustmentPanel(self)
        self.turns_panel.setFixedWidth(100)
        self.turns_panel.setFixedHeight(100)
        self.turns_panel.setContentsMargins(0, 0, 0, 0)
        self.turns_panel.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
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
        self.pictograph_layout.addWidget(self.turns_panel)
        self.layout.addLayout(self.pictograph_layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)

    def render_pictograph(self, pictograph: Pictograph) -> None:
        self.GE_pictograph.view.setScene(pictograph)

    def resize_graph_editor(self):
        self.GE_pictograph_container.resize_GE_pictograph_container()
