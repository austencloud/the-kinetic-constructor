from multiprocessing import parent_process
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QTabWidget
from widgets.ig_tab.ig_filter_frame.ig_color_attr_panel import IGColorAttrPanel

from widgets.ig_tab.ig_filter_frame.ig_motion_attr_panel import IGMotionAttrPanel

if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab


class IGFilterTab(QTabWidget):
    def __init__(self, ig_tab: "IGTab") -> None:
        super().__init__(ig_tab)
        self.ig_tab = ig_tab
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.motion_attr_panel = IGMotionAttrPanel(self.ig_tab)
        self.color_attr_panel = IGColorAttrPanel(self.ig_tab)
        self.addTab(self.motion_attr_panel, "Filter by Motion Type")
        self.addTab(self.color_attr_panel, "Filter by Colors")
