from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from base_widgets.base_pictograph.pictograph_view import PictographView

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.codex.codex import Codex
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class CodexPictographView(PictographView):
    def __init__(self, pictograph: "BasePictograph", codex: "Codex") -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.codex = codex
        self.setStyleSheet("border: 1px solid black;")

    def resizeEvent(self, event):
        size = self.codex.learn_tab.main_widget.width() // 16
        self.setMinimumSize(size, size)
        self.setMaximumSize(size, size)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        super().resizeEvent(event)
