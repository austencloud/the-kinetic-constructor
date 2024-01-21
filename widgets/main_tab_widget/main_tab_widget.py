from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QTabWidget,
)

from widgets.codex.codex import Codex


if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class MainTabWidget(QTabWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.setStyleSheet(self.get_main_tab_stylesheet())
        self.codex = Codex(self)
        self.tabs = [self.codex]
        self.addTab(self.codex, "Codex")
        # self.addTab(graph_editor_tab, "Graph Editor")
        # self.addTab(option_picker_tab, "Option Picker")

    def get_main_tab_stylesheet(self) -> str:
        return """
            QTabWidget::pane {
                border: 1px solid black;
                background: white;
            }
            QTabWidget::tab-bar:top {
                top: 1px;
            }
            QTabWidget::tab-bar:bottom {
                bottom: 1px;
            }
            QTabWidget::tab-bar:left {
                right: 1px;
            }
            QTabWidget::tab-bar:right {
                left: 1px;
            }
            QTabBar::tab {
                border: 1px solid black;
            }
            QTabBar::tab:selected {
                background: white;
            }
            QTabBar::tab:!selected {
                background: silver;
            }
            QTabBar::tab:!selected:hover {
                background: #999;
            }
            QTabBar::tab:top:!selected {
                margin-top: 3px;
            }
            QTabBar::tab:bottom:!selected {
                margin-bottom: 3px;
            }
            QTabBar::tab:top, QTabBar::tab:bottom {
                min-width: 8ex;
                margin-right: -1px;
                padding: 5px 10px 5px 10px;
            }
            QTabBar::tab:top:selected {
                border-bottom-color: none;
            }
            QTabBar::tab:bottom:selected {
                border-top-color: none;
            }
            QTabBar::tab:top:last, QTabBar::tab:bottom:last,
            QTabBar::tab:top:only-one, QTabBar::tab:bottom:only-one {
                margin-right: 0;
            }
            QTabBar::tab:left:!selected {
                margin-right: 3px;
            }
            QTabBar::tab:right:!selected {
                margin-left: 3px;
            }
            QTabBar::tab:left, QTabBar::tab:right {
                min-height: 8ex;
                margin-bottom: -1px;
                padding: 10px 5px 10px 5px;
            }
            QTabBar::tab:left:selected {
                border-left-color: none;
            }
            QTabBar::tab:right:selected {
                border-right-color: none;
            }
            QTabBar::tab:left:last, QTabBar::tab:right:last,
            QTabBar::tab:left:only-one, QTabBar::tab:right:only-one {
                margin-bottom: 0;
            }
            """
