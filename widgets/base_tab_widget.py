from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QTabWidget


if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class BaseTabWidget(QTabWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.setStyleSheet(self.get_tab_stylesheet())

    def get_tab_stylesheet(self) -> str:
        return """
            QTabWidget::pane {
                border: 1px solid black;
            }
            GE_TurnsBox {
                background-color: white;
            }
            GE_StartPosOriPickerBox {
                background-color: white;
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
                background: silver;
                font: 16pt "Calibri"; /* Keep font size consistent */
                color: black;
            }
            QTabBar::tab:selected {
                background: white;
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

            """
