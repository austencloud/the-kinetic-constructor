from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from widgets.graph_editor.GE_turns_button_manager import GE_TurnsButtonManager
from widgets.graph_editor.GE_turns_widget_display_manager import (
    GE_TurnsWidgetDisplayManager,
)
from widgets.graph_editor.components.GE_turns_adjustment_manager import (
    GE_TurnsAdjustmentManager,
)
from widgets.graph_editor.components.GE_turns_direct_set_manager import (
    GE_TurnsDirectSetManager,
)
from widgets.graph_editor.components.GE_turns_updater import GE_TurnsUpdater
from widgets.turns_box.turns_box_widgets.turns_widget.managers.motion_relevance_checker import (
    CodexMotionRelevanceChecker,
)


if TYPE_CHECKING:
    from .GE_turns_box import GE_TurnsBox


class GE_TurnsWidget(QWidget):
    def __init__(self, turns_box: "GE_TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self._setup_layout()
        self._setup_components()
        self._setup_ui()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 4, 0, 0)
        self.layout.setSpacing(0)

    def _setup_components(self):
        self.adjustment_manager = GE_TurnsAdjustmentManager(self)
        self.direct_set_manager = GE_TurnsDirectSetManager(self)
        self.display_manager = GE_TurnsWidgetDisplayManager(self)
        self.button_manager = GE_TurnsButtonManager(self)
        self.updater = GE_TurnsUpdater(self)

    def _setup_ui(self) -> None:
        self.button_manager.setup_adjust_turns_buttons()
        self.display_manager.setup_display_components()
        self.direct_set_manager.setup_direct_set_buttons()

    ### WIDGETS ###

    def resize_GE_turns_widget(self) -> None:
        self.display_manager.update_turn_display()
        self.display_manager.update_adjust_turns_button_size()
