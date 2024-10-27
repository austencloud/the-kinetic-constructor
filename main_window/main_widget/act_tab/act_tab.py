from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from main_window.main_widget.act_browser import ActBrowser
from .act_sheet import ActSheet

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class ActTab(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget

        self.act_sheet = ActSheet(self.main_widget)
        self.act_browser = ActBrowser(self)

        self._setup_layout()

    def _setup_layout(self):
        layout = QHBoxLayout(self)
        layout.addWidget(self.act_sheet, 1)
        layout.addWidget(self.act_browser, 1)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.act_sheet.resize_act_sheet()
        self.act_browser.resize_browser()

    def showEvent(self, event):
        if not self.act_sheet.initialized:
            self.act_sheet.resize_act_sheet()
        self.act_browser.resize_browser()
        super().showEvent(event)