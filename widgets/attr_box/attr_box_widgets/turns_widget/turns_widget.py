from PyQt6.QtWidgets import QVBoxLayout
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
    from attr_box.attr_box import AttrBox


class TurnsWidget(AttrBoxWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.vbox_layout: QVBoxLayout = QVBoxLayout(self)
        self.turn_direct_set_manager = TurnDirectSetManager(self)
        self.turn_adjust_manager = TurnAdjustManager(self)
        self.turns_display_manager = TurnDisplayManager(self)
        self.button_manager = TurnsButtonManager(self)
        self.relevance_checker = MotionRelevanceChecker(attr_box)
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
