from typing import TYPE_CHECKING, Dict, List, Union
from PyQt6.QtGui import QPixmap
from Enums import Color
from objects.motion.motion import Motion
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.start_end_ori_widget import (
    StartEndOriWidget,
)
from widgets.graph_editor_tab.attr_panel.bast_attr_box import BaseAttrBox
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.header_widget import (
    HeaderWidget,
)
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.start_end_loc_widget import (
    StartEndLocWidget,
)
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.base_turns_widget import (
    BaseTurnsWidget,
)
from widgets.graph_editor_tab.attr_panel.custom_button import CustomButton
from widgets.image_generator_tab.ig_turns_widget import IGTurnsWidget

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_attr_panel import IGAttrPanel
    from objects.pictograph.pictograph import Pictograph

    from widgets.graph_editor_tab.attr_panel.base_attr_panel import (
        BaseAttrPanel,
    )
from PyQt6.QtGui import QPixmap, QFont


class IGAttrBox(BaseAttrBox):
    def __init__(
        self,
        ig_attr_panel: "IGAttrPanel",
        pictographs: List["Pictograph"],
        color: Color,
    ) -> None:
        super().__init__(
            ig_attr_panel, None, color
        )  # Note the None for the single pictograph
        self.ig_attr_panel = ig_attr_panel
        self.pictographs: Dict[str, Pictograph] = pictographs
        self.color = color
        self.font_size = self.width() // 10
        self.widgets: List[AttrBoxWidget] = []
        self.combobox_border = 2
        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache
        self._setup_widgets()

    def _setup_widgets(self) -> None:  # add common widgets
        self.header_widget = HeaderWidget(self)
        # self.start_end_ori_widget = StartEndOriWidget(self)
        self.turns_widget = IGTurnsWidget(self)

        self.layout.addWidget(self.header_widget)
        # self.layout.addWidget(self.start_end_ori_widget)
        self.layout.addWidget(self.turns_widget)

    def resize_ig_attr_box(self) -> None:
        self.setMinimumWidth(int(self.ig_attr_panel.ig_tab.width() / 3))
        self.setMaximumWidth(int(self.ig_attr_panel.ig_tab.width() / 3))

        for button in self.findChildren(CustomButton):
            button.update_custom_button_size(int(self.width() / 8))

        self.header_widget.resize_header_widget()
        self.turns_widget.resize_turns_widget()
        self.header_widget.header_label.setFont(QFont("Arial", int(self.width() / 15)))

    def update_attr_box(self, motion: Motion) -> None:
        if motion.prop_rot_dir:
            self.turns_widget._update_turnbox(motion.turns)
