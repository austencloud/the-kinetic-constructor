from PyQt6.QtGui import QPalette, QColor, QFont, QCursor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTabWidget, QPushButton


class SettingsDialogStyler:
    @staticmethod
    def style_tab_widget(tab_widget: QTabWidget):
        # Tab widget palette
        palette = tab_widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#F5F5F5"))
        tab_widget.setPalette(palette)

        # Customize the tab bar
        tab_bar = tab_widget.tabBar()
        tab_bar.setFont(SettingsDialogStyler._get_tab_font())
        tab_bar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Iterate through each tab and adjust margins for spacing
        for i in range(tab_bar.count()):
            tab_bar.setTabTextColor(i, QColor("#333333"))
            tab_bar.setTabData(i, {"hovered": False})  # Store hover state

    @staticmethod
    def style_button(button: QPushButton):
        # Default button styling
        button.setFont(SettingsDialogStyler._get_button_font())
        button.setStyleSheet("""
            QPushButton {
                background-color: #66B2FF;
                color: white;
                border-radius: 10px;
                padding: 10px 15px;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)

    @staticmethod
    def _get_tab_font():
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        return font

    @staticmethod
    def _get_button_font():
        font = QFont()
        font.setPointSize(14)
        return font
