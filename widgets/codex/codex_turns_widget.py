from PyQt6.QtWidgets import QVBoxLayout, QLabel
from typing import TYPE_CHECKING, Union
from ..turns_box.turns_box_widgets.turns_widget.managers.motion_relevance_checker import MotionRelevanceChecker
from ..turns_box.turns_box_widgets.turns_widget.managers.turns_button_manager import TurnsButtonManager
from ..turns_box.turns_box_widgets.turns_widget.managers.turns_adjustment_manager import TurnsAdjustmentManager
from ..turns_box.turns_box_widgets.turns_widget.managers.turns_updater import TurnsUpdater
from ..turns_box.turns_box_widgets.turns_widget.managers.turns_display_manager import TurnDisplayManager
from ..turns_box.turns_box_widgets.turns_widget.managers.turns_direct_set_manager import TurnsDirectSetManager
from .codex_letter_button_frame.components.codex_turns_box_widget import (
    CodexTurnsBoxWidget,
)
from .codex_letter_button_frame.components.codex_turns_box_widget import (
    CodexTurnsBoxWidget,
)

if TYPE_CHECKING:
    from turns_box.turns_box import TurnsBox


class CodexTurnsWidget(CodexTurnsBoxWidget):
    def __init__(self, turns_box: "TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self.turns_label: QLabel = None
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 4, 0, 0)
        self.layout.setSpacing(0)
        self.direct_set_manager = TurnsDirectSetManager(self)
        self.display_manager = TurnDisplayManager(self)
        self.button_manager = TurnsButtonManager(self)
        self.relevance_checker = MotionRelevanceChecker(turns_box)
        self.adjustment_manager = TurnsAdjustmentManager(self)
        self.updater = TurnsUpdater(self)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.button_manager.setup_adjust_turns_buttons()
        self.display_manager.setup_display_components()
        self.direct_set_manager.setup_direct_set_buttons()

    def _convert_turns_from_str_to_num(self, turns) -> Union[int, float]:
        return int(turns) if turns in ["0", "1", "2", "3"] else float(turns)

    def resize_turns_widget(self) -> None:
        self.display_manager.update_turn_display()
        self.display_manager.update_adjust_turns_button_size()
