from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QWidget

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class NavigationSidebar(QWidget):
    def __init__(self, browser: "DictionaryBrowser"):
        super().__init__()
        self.browser = browser
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.buttons: list[QPushButton] = []

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
            self.layout.addWidget(button)
            self.buttons.append(button)
        # Ensure the sidebar is refreshed and visible
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
            content_widget = scroll_area.widget()

            # Get the global position of the header widget
            header_global_pos = header.mapToGlobal(header.pos())

            # Convert the global position to a position relative to the scroll area's viewport
            header_viewport_pos = scroll_area.viewport().mapFromGlobal(
                header_global_pos
            )

            # Calculate the y-coordinate to scroll to, aiming to align the header at the top of the viewport
            # Subtracting the height of the header ensures it aligns exactly at the top
            vertical_pos = header_viewport_pos.y()

            # Use ensureWidgetVisible with calculated x and y margins to place the header at the top
            scroll_area.ensureWidgetVisible(header, 0, vertical_pos)
            # get the location of the header section's top in the overall scroll area's widget
            header_top = scroll_area.mapFromParent(header_global_pos).y()
            # get the location of the scroll area widget's top in the overall scroll area's widget
            scroll_area_top = scroll_area.mapFromParent(scroll_area.pos()).y()
            # ge tthe distance between the top of the header and the top of the scroll area
            distance = header_top - scroll_area_top
            # scroll up until that disntace is at the top of the scroll area
            scroll_area.verticalScrollBar().setValue(
                scroll_area.verticalScrollBar().value() + distance
            )

    def resizeEvent(self, event):
        for button in self.buttons:
            self.style_button(button)
        super().resizeEvent(event)
