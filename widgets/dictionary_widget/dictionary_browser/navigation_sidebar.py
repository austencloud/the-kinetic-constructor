from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QWidget, QScrollArea
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, QPoint

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class NavigationSidebar(QWidget):
    def __init__(self, browser: "DictionaryBrowser"):
        super().__init__()
        self.browser = browser
        self._setup_scroll_area()
        self.layout: QVBoxLayout = QVBoxLayout(self.scroll_content)
        self.buttons: list[QPushButton] = []

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

    def _setup_scroll_area(self):
        self.scroll_content = QWidget()
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setStyleSheet("background: transparent;")

    def update_sidebar(self, sections):
        # Clear existing buttons
        for button in self.buttons:
            self.layout.removeWidget(button)
            button.deleteLater()
        self.buttons.clear()

        # Create new buttons for each section
        for section in sections:
            button = QPushButton(str(section))
            button.clicked.connect(
                lambda checked, sec=section: self.scroll_to_section(sec)
            )
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.layout.addWidget(button)
            self.buttons.append(button)

        # Ensure the sidebar is refreshed and visible
        self.style_all_buttons()
        self.show()

    def style_button(self, button: QPushButton):
        font_size = self.browser.width() // 30
        button.setStyleSheet(
            f"""
            QPushButton {{
                background: transparent;
                border: none;
                font-size: {font_size}px;
                font-weight: bold;
                color: #333;
                padding: 5px;
                text-align: center;
            }}
            QPushButton:hover {{
                background: #f0f0f0;
            }}
        """
        )

    def scroll_to_section(self, section):
        header = self.browser.scroll_widget.section_headers.get(section)
        if header:
            scroll_area = self.browser.scroll_widget.scroll_area

            # Get the global position of the header widget
            header_global_pos = header.mapToGlobal(QPoint(0, 0))

            # Convert the global position to a position relative to the scroll area's content widget
            content_widget_pos = scroll_area.widget().mapFromGlobal(header_global_pos)

            # Calculate the y-coordinate to scroll to, aiming to align the header at the top of the viewport
            vertical_pos = content_widget_pos.y()

            # Set the scrollbar value to the calculated vertical position
            scroll_area.verticalScrollBar().setValue(vertical_pos)

    def style_all_buttons(self):
        for button in self.buttons:
            self.style_button(button)

    def resizeEvent(self, event):
        self.style_all_buttons()
        super().resizeEvent(event)
