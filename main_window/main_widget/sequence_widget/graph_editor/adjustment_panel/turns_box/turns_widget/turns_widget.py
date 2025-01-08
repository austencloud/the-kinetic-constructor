from PyQt6.QtWidgets import QVBoxLayout, QWidget
from typing import TYPE_CHECKING
from .turns_text_label import TurnsTextLabel
from .motion_type_setter import MotionTypeSetter
from .direct_set_dialog.direct_set_turns_dialog import DirectSetTurnsDialog
from .turns_display_frame.turns_display_frame import TurnsDisplayFrame
from .turns_adjuster import TurnsAdjuster
from .turns_updater import JsonTurnsUpdater
from .motion_type_label_widget import MotionTypeLabel

if TYPE_CHECKING:
    from ..turns_box import TurnsBox


class TurnsWidget(QWidget):
    def __init__(self, turns_box: "TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self._setup_components()
        self._setup_layout()

    def _setup_components(self) -> None:
        self.adjustment_manager = TurnsAdjuster(self)
        self.json_turns_updater = JsonTurnsUpdater(self)
        self.display_frame = TurnsDisplayFrame(self)
        self.direct_set_dialog = DirectSetTurnsDialog(self)
        self.turns_text = TurnsTextLabel(self)
        self.motion_type_label = MotionTypeLabel(self)
        self.motion_type_setter = MotionTypeSetter(self)

    def _setup_layout(self) -> None:
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.turns_text)
        layout.addStretch(1)
        layout.addWidget(self.display_frame)
        layout.addStretch(2)
        layout.addWidget(self.motion_type_label)
        layout.addStretch(2)
