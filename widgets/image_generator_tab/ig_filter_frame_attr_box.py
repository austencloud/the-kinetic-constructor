from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtGui import QPixmap
from Enums import Color
from objects.motion.motion import Motion
from widgets.graph_editor_tab.attr_panel.attr_box import AttrBox
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from widgets.graph_editor_tab.attr_panel.attr_panel import (
        AttrPanel,
    )


class IGFilterFrameAttrBox(AttrBox):
    def __init__(
        self, attr_panel: "AttrPanel", pictographs: List["Pictograph"], color: Color
    ) -> None:
        super().__init__(
            attr_panel, None, color
        )  # Note the None for the single pictograph
        self.pictographs = pictographs

        self.attr_panel = attr_panel
        self.pictographs = pictographs
        self.color = color
        self.font_size = self.width() // 10
        self.widgets: List[AttrBoxWidget] = []
        self.combobox_border = 2
        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache


    def update_attr_box(self, motion: Motion = None) -> None:
        for pictograph in self.pictographs:
            pass  

