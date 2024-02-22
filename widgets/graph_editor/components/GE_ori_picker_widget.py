from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from widgets.graph_editor.components.GE_ori_picker_button_manager import (
    GE_StartPosOriPickerButtonManager,
)
from widgets.graph_editor.components.GE_ori_picker_display_manager import (
    GE_StartPosOriPickerDisplayManager,
)
from widgets.graph_editor.components.GE_start_pos_ori_updater import (
    GE_StartPosOriPickerUpdater,
)


if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_start_pos_ori_picker import (
        GE_StartPosOriPickerBox,
    )


class GE_StartPosOriPickerWidget(QWidget):
    def __init__(self, ori_picker_box: "GE_StartPosOriPickerBox") -> None:
        super().__init__(ori_picker_box)
        self.ori_picker_box = ori_picker_box
        self._setup_layout()
        self._setup_components()
        self._setup_ui()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 4, 0, 0)
        self.layout.setSpacing(0)

    def _setup_components(self):
        self.display_manager = GE_StartPosOriPickerDisplayManager(self)
        self.turns_button_manager = GE_StartPosOriPickerButtonManager(self)
        self.updater = GE_StartPosOriPickerUpdater(self)

    def _setup_ui(self) -> None:
        self.turns_button_manager.setup_adjust_turns_buttons()
        self.display_manager.setup_display_components()

    ### WIDGETS ###

    def resize_GE_ori_picker_widget(self) -> None:
        self.display_manager.update_ori_picker_display()
