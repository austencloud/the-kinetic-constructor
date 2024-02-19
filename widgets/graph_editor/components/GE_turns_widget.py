from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
    QHBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from widgets.graph_editor.GE_turns_button_manager import GE_TurnsButtonManager
from widgets.graph_editor.GE_turns_widget_display_manager import (
    GE_TurnsWidgetDisplayManager,
)
from widgets.graph_editor.components.GE_turns_adjustment_manager import (
    GE_TurnsAdjustmentManager,
)
from widgets.turns_box.turns_box_widgets.turns_widget.managers.turn_direct_set_manager import (
    TurnDirectSetManager,
)
from widgets.turns_box.turns_box_widgets.turns_widget.managers.turns_updater import (
    TurnsUpdater,
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
        self.layout.setContentsMargins(0, 4, 0, 0)
        self.layout.setSpacing(0)

    def _setup_components(self):
        self.direct_set_manager = TurnDirectSetManager(self)
        self.display_manager = GE_TurnsWidgetDisplayManager(self)
        self.button_manager = GE_TurnsButtonManager(self)
        self.adjustment_manager = GE_TurnsAdjustmentManager(self)
        self.updater = TurnsUpdater(self)

    def _setup_ui(self) -> None:
        self.button_manager.setup_adjust_turns_buttons()
        self.display_manager.setup_display_components()
        self.direct_set_manager.setup_direct_set_buttons()

    ### WIDGETS ###

    def resize_GE_turns_widget(self) -> None:
        self.display_manager.update_turn_display()
        self.display_manager.update_adjust_turns_button_size()
