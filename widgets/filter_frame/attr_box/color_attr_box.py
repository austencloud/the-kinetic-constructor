from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtGui import QPixmap
from constants import COLOR, OPP, SAME
from objects.motion.motion import Motion
from utilities.TypeChecking.TypeChecking import Colors
from .base_attr_box import BaseAttrBox
from .attr_box_widgets.base_attr_box_widget import BaseAttrBoxWidget
from .attr_box_widgets.header_widgets.color_header_widget import ColorHeaderWidget
from .attr_box_widgets.turns_widgets.color_turns_widget import ColorTurnsWidget
from .attr_box_widgets.vtg_dir_widget import VtgDirWidget
if TYPE_CHECKING:
    from widgets.filter_frame.attr_panel.color_attr_panel import ColorAttrPanel
    from objects.pictograph.pictograph import Pictograph

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout


class ColorAttrBox(BaseAttrBox):
    def __init__(
        self,
        attr_panel: "ColorAttrPanel",
        pictographs: List["Pictograph"],
        color: Colors,
    ) -> None:
        super().__init__(attr_panel, None)  # Note the None for the single pictograph
        self.attr_panel = attr_panel
        self.color = color
        self.pictographs: Dict[str, Pictograph] = pictographs
        self.font_size = self.width() // 10
        self.widgets: List[BaseAttrBoxWidget] = []
        self.combobox_border = 2
        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache
        self.hbox_layout = QHBoxLayout()
        self.vbox2 = QVBoxLayout()
        self.layout: QHBoxLayout = self.hbox_layout
        self.hbox_layout.addLayout(self.vbox_layout)
        self._setup_widgets()
        self.same_button = self.vtg_dir_widget.same_button
        self.opp_button = self.vtg_dir_widget.opp_button
        self.same_opp_buttons = [self.same_button, self.opp_button]
        self.attribute_type = COLOR
        self.vtg_dir_btn_state = {SAME: True, OPP: False}

    def _setup_widgets(self) -> None:  # add common widgets
        self.header_widget = ColorHeaderWidget(self, self.color)
        self.vtg_dir_widget = VtgDirWidget(self)
        self.turns_widget = ColorTurnsWidget(self)
        self.vbox_layout.addWidget(self.header_widget, 1)
        self.vbox_layout.addWidget(self.turns_widget, 2)
        self.hbox_layout.addWidget(self.vtg_dir_widget, 2)
        self.setLayout(self.hbox_layout)

    def resize_ig_color_attr_box(self) -> None:
        self.setMinimumWidth(int(self.attr_panel.ig_tab.width() / 3))
        self.setMaximumWidth(int(self.attr_panel.ig_tab.width() / 3))
        self.turns_widget.resize_turns_widget()
        self.vtg_dir_widget.resize_prop_rot_dir_widget()

    def update_attr_box(self, motion: Motion) -> None:
        for pictograph in self.pictographs.values():
            for motion in pictograph.motions.values():
                self.turns_widget.update_turns_display(motion.turns)

    def get_pictographs(self) -> List["Pictograph"]:
        return list(self.pictographs.values())
