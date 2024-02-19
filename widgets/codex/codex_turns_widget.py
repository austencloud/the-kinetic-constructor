from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget
from typing import TYPE_CHECKING, Union
from ..turns_box.turns_box_widgets.turns_widget.managers.motion_relevance_checker import (
    MotionRelevanceChecker,
)
from ..turns_box.turns_box_widgets.turns_widget.managers.turns_button_manager import (
    CodexTurnsButtonManager,
)
from ..turns_box.turns_box_widgets.turns_widget.managers.turns_adjustment_manager import (
    TurnsAdjustmentManager,
)
from ..turns_box.turns_box_widgets.turns_widget.managers.turns_updater import (
    TurnsUpdater,
)
from ..turns_box.turns_box_widgets.turns_widget.managers.codex_turns_widget_display_manager import (
    CodexTurnsWidgetDisplayManager,
)
from ..turns_box.turns_box_widgets.turns_widget.managers.turns_direct_set_manager import (
    TurnsDirectSetManager,
)
from .codex_turns_box_widget import (
    CodexWidget,
)
from .codex_turns_box_widget import (
    CodexWidget,
)

if TYPE_CHECKING:
    from widgets.turns_box.codex_turns_box import CodexTurnsBox


class CodexTurnsWidget(QWidget):
    def __init__(self, turns_box: "CodexTurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self.turns_label: QLabel = None
        self._setup_layout()
        self._setup_components(turns_box)
        self._setup_ui()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 4, 0, 0)
        self.layout.setSpacing(0)

    def _setup_components(self, turns_box):
        self.direct_set_manager = TurnsDirectSetManager(self)
        self.display_manager = CodexTurnsWidgetDisplayManager(self)
        self.button_manager = CodexTurnsButtonManager(self)
        self.relevance_checker = MotionRelevanceChecker(turns_box)
        self.adjustment_manager = TurnsAdjustmentManager(self)
        self.updater = TurnsUpdater(self)

    def _setup_ui(self) -> None:
        self.button_manager.setup_adjust_turns_buttons()
        self.display_manager.setup_display_components()
        self.direct_set_manager.setup_direct_set_buttons()

    def _convert_turns_from_str_to_num(self, turns) -> Union[int, float]:
        return int(turns) if turns in ["0", "1", "2", "3"] else float(turns)

    def resize_turns_widget(self) -> None:
        self.display_manager.update_turn_display()
        self.display_manager.update_adjust_turns_button_size()
