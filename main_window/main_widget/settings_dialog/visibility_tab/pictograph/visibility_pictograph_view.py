from PyQt6.QtCore import QEvent
from typing import TYPE_CHECKING
from base_widgets.base_pictograph.pictograph_view import PictographView
from .visibility_pictograph_interaction_manager import (
    VisibilityPictographInteractionManager,
)

if TYPE_CHECKING:
    from .visibility_pictograph import VisibilityPictograph
    from ..visibility_tab import VisibilityTab


class VisibilityPictographView(PictographView):

    def __init__(
        self, visibility_tab: "VisibilityTab", pictograph: "VisibilityPictograph"
    ):
        self.visibility_tab = visibility_tab
        self.visibility_settings = visibility_tab.settings
        self.main_widget = visibility_tab.main_widget
        super().__init__(pictograph)

        self.interaction_manager = VisibilityPictographInteractionManager(self)
        self.setStyleSheet("border: 2px solid black;")

    def resizeEvent(self, event: QEvent):
        available_width = (
            self.visibility_tab.dialog.width()
            - self.visibility_tab.buttons_widget.width()
        )
        size = int(available_width * 0.7)
        self.setFixedSize(size, size)
        super().resizeEvent(event)
