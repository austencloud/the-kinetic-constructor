from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget

class MainWidgetTabBarStyler:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget
        self.update_measurements()

    def update_measurements(self):
        self.width = self.main_widget.width()
        self.height = self.main_widget.height()
        self.font_size = int(self.height * 0.02)
        self.padding_vertical = int(self.height * 0.005)
        self.padding_horizontal = int(self.width * 0.005)
        self.tab_width = int(self.width * 0.1)
        self.tab_height = int(self.height * 0.02)

    def get_tab_stylesheet(self) -> str:
        self.update_measurements()
        return f"""
            QTabWidget::pane {{
                border: none; /* Remove the border */
            }}
            QTabWidget::tab-bar {{
                alignment: center; /* Center the tab bar */
            }}
            QTabBar::tab {{
                background: silver;
                font-size: {self.font_size}px;  /* Dynamically set font size */
                padding: {self.padding_vertical}px {self.padding_horizontal}px;  /* Dynamically set padding */
                color: black;
                border-radius: 5px;
            }}
            QTabBar::tab:selected {{
                background: white;
                border: 2px solid #0078D7;  /* Add a border to the selected tab */
            }}
            QTabBar::tab:!selected:hover {{
                background: #999;  /* Change background color when hovering over unselected tab */
            }}
            QTabBar::tab {{
                min-width: {self.tab_width}px;  /* Dynamically set tab width */
                min-height: {self.tab_height}px;  /* Dynamically set tab height */
            }}
            QTabBar::tab:selected {{
                border-bottom-color: none;
            }}
        """
