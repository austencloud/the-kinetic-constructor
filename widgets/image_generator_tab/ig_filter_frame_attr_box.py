from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtGui import QPixmap
from Enums import Color
from objects.motion.motion import Motion
from widgets.graph_editor_tab.attr_panel.attr_box import BaseAttrBox
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.header_widget import HeaderWidget
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.start_end_widget import StartEndWidget
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.turns_widget import TurnsWidget

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from widgets.graph_editor_tab.attr_panel.attr_panel import (
        AttrPanel,
    )


class IGFilterFrameAttrBox(BaseAttrBox):
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
        self._setup_widgets()

    def _setup_widgets(self) -> None:  # add common widgets
        self.header_widget = HeaderWidget(self)
        self.start_end_widget = StartEndWidget(self)
        self.turns_widget = TurnsWidget(self)

        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.start_end_widget)
        self.layout.addWidget(self.turns_widget)