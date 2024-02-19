from typing import TYPE_CHECKING
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout

from widgets.animator.components.animated_pictograph import (
    AnimatedPictograph,
    AnimatedPictographView,
)
from widgets.animator.components.animated_pictograph_container import (
    AnimatedPictographContainer,
)
from widgets.graph_editor.components.GE_turns_panel import GE_AdjustmentPanel


from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_modifier import SequenceModifierTab


class Animator(QFrame):
    def __init__(self, sequence_modifier: "SequenceModifierTab") -> None:
        super().__init__()
        self.sequence_modifier = sequence_modifier
        self.main_widget = sequence_modifier.main_widget

        self._setup_animated_pictograph()
        # self._setup_adjustment_panel()
        self._setup_layout()

    def _setup_animated_pictograph(self):
        self.animated_pictograph = AnimatedPictograph(self)
        self.animated_pictograph_view = AnimatedPictographView(
            self.animated_pictograph, self
        )
        self.animated_pictograph_container = AnimatedPictographContainer(
            self, self.animated_pictograph_view
        )

    def _setup_adjustment_panel(self):
        self.turns_panel = GE_AdjustmentPanel(self)
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
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.pictograph_layout = QVBoxLayout()
        self.pictograph_layout.addWidget(self.animated_pictograph.view)
        self.layout.addLayout(self.pictograph_layout)

        # self.turns_panel_layout = QVBoxLayout()
        # self.turns_panel_layout.addWidget(self.turns_panel)
        # self.layout.addLayout(self.turns_panel_layout)

        self.setLayout(self.layout)

    def render_pictograph(self, pictograph: Pictograph) -> None:
        self.animated_pictograph.view.setScene(pictograph)

    def resize_animator(self):
        self.animated_pictograph_container.resize_animated_pictograph_container()
