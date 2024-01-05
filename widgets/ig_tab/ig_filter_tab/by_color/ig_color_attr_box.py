from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtGui import QPixmap
from objects.motion.motion import Motion
from utilities.TypeChecking.TypeChecking import Colors
from widgets.attr_box_widgets.base_attr_box_widget import BaseAttrBoxWidget
from widgets.attr_panel.bast_attr_box import BaseAttrBox
from widgets.ig_tab.ig_filter_tab.by_color.ig_color_header_widget import IGColorHeaderWidget
from widgets.ig_tab.ig_filter_tab.by_color.ig_color_turns_widget import IGColorTurnsWidget

from widgets.ig_tab.ig_filter_tab.by_motion_type.ig_motion_type_header_widget import (
    IGMotionTypeHeaderWidget,
)

if TYPE_CHECKING:
    from widgets.ig_tab.ig_filter_tab.by_color.ig_color_attr_panel import (
        IGColorAttrPanel,
    )
    from objects.pictograph.pictograph import Pictograph

from PyQt6.QtGui import QPixmap, QFont


class IGColorAttrBox(BaseAttrBox):
    def __init__(
        self,
        attr_panel: "IGColorAttrPanel",
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
        self._setup_widgets()


    def _setup_widgets(self) -> None:  # add common widgets
        self.header_widget = IGColorHeaderWidget(self, self.color)
        self.turns_widget = IGColorTurnsWidget(self)

        self.layout.addWidget(self.header_widget, 1)
        self.layout.addWidget(self.turns_widget, 2)

    def resize_ig_color_attr_box(self) -> None:
        self.setMinimumWidth(int(self.attr_panel.ig_tab.width() / 6))
        self.setMaximumWidth(int(self.attr_panel.ig_tab.width() / 6))
        self.header_widget.resize_header_widget()
        self.turns_widget.resize_turns_widget()
        self.header_widget.header_label.setFont(QFont("Arial", int(self.width() / 10)))

    def update_attr_box(self, motion: Motion) -> None:
        for pictograph in self.pictographs.values():
            for motion in pictograph.motions.values():
                self.turns_widget._update_turnbox(motion.turns)

    def get_pictographs(self) -> List["Pictograph"]:
        return list(self.pictographs.values())
