from PyQt6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QFrame
from typing import TYPE_CHECKING, Union
from .managers.motion_relevance_checker import MotionRelevanceChecker
from .managers.turns_widget_rot_dir_manager import TurnsWidgetRotDirManager
from .managers.turn_adjust_manager import TurnAdjustManager
from .managers.turns_button_manager import TurnsButtonManager
from .managers.turn_adjustment_display_manager import TurnsAdjustmentDisplayManager
from .managers.turns_updater import TurnsUpdater
from .managers.turns_display_manager import TurnDisplayManager
from .managers.turn_direct_set_manager import TurnDirectSetManager
from ..base_attr_box_widget import AttrBoxWidget
from ..base_attr_box_widget import AttrBoxWidget

if TYPE_CHECKING:
    from turns_box.turns_box import TurnsBox


class TurnsWidget(AttrBoxWidget):
    def __init__(self, turns_box: "TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self.turns_label: QLabel = None
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.turn_direct_set_manager = TurnDirectSetManager(self)
        self.turn_adjust_manager = TurnAdjustManager(self)
        self.turns_display_manager = TurnDisplayManager(self)
        self.button_manager = TurnsButtonManager(self)
        self.relevance_checker = MotionRelevanceChecker(turns_box)
        self.updater = TurnsUpdater(self)
        self.rotation_direction_manager = TurnsWidgetRotDirManager(self)
        self.display_manager = TurnsAdjustmentDisplayManager(self)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.turn_adjust_manager.setup_adjust_turns_buttons()
        self.turns_display_manager.setup_display_components()
        self.turn_direct_set_manager.setup_direct_set_buttons()

    def _convert_turns_from_str_to_num(self, turns) -> Union[int, float]:
        return int(turns) if turns in ["0", "1", "2", "3"] else float(turns)

    def resize_turns_widget(self) -> None:
        self.turns_display_manager.update_turn_display()
        self.turns_display_manager.update_adjust_turns_button_size()
