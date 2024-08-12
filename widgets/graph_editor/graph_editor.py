from typing import TYPE_CHECKING
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy
from widgets.graph_editor.components.GE_adjustment_panel import GE_AdjustmentPanel
from widgets.pictograph.pictograph import Pictograph

from widgets.graph_editor.components.GE_pictograph_view import (
    GE_BlankPictograph,
    GE_PictographView,
)
from widgets.graph_editor.components.GE_pictograph_container import (
    GE_PictographContainer,
)

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class GraphEditor(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__()
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget
        self._setup_pictograph()
        self._setup_adjustment_panel()
        self._setup_layout()

    def _setup_pictograph(self) -> None:
        self.GE_pictograph = GE_BlankPictograph(self)
        self.GE_pictograph_view = GE_PictographView(self, self.GE_pictograph)
        self.GE_pictograph_container = GE_PictographContainer(
            self, self.GE_pictograph_view
        )

    def _setup_adjustment_panel(self) -> None:
        self.adjustment_panel = GE_AdjustmentPanel(self)
        self.adjustment_panel.setContentsMargins(0, 0, 0, 0)

    def _setup_frame_style(self) -> None:
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setLineWidth(1)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.setPalette(palette)

    def _setup_layout(self) -> None:
        self._setup_pictograph_layout()
        self._setup_adjustment_panel_layout()

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.layout.addLayout(self.pictograph_layout)
        self.layout.addLayout(self.adjustment_panel_layout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def _setup_adjustment_panel_layout(self) -> None:
        self.adjustment_panel_layout = QVBoxLayout()
        self.adjustment_panel_layout.addWidget(self.adjustment_panel)
        self.adjustment_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.adjustment_panel_layout.setSpacing(0)

    def _setup_pictograph_layout(self) -> None:
        self.pictograph_layout = QVBoxLayout()
        self.pictograph_layout.addWidget(self.GE_pictograph_container)
        self.pictograph_layout.setContentsMargins(0, 0, 0, 0)
        self.pictograph_layout.setSpacing(0)
        self.pictograph_layout.setStretch(1, 1)

    def update_GE_pictograph(self, pictograph: Pictograph) -> None:
        self.GE_pictograph_view.set_scene(pictograph)
        self.GE_pictograph = pictograph

    def resize_graph_editor(self) -> None:
        self.setFixedHeight(int(self.sequence_widget.height() // 3))
        self.GE_pictograph_container.resize_GE_pictograph_container()
        self.adjustment_panel.update_adjustment_panel()
