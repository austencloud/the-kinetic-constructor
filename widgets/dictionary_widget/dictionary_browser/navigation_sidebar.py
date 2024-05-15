from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QWidget

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import DictionaryBrowser


class NavigationSidebar(QWidget):
    def __init__(self, browser: "DictionaryBrowser"):
        super().__init__()
        self.browser = browser
        self.layout:QVBoxLayout = QVBoxLayout(self)
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

    def scroll_to_section(self, section):
        # Find the header widget for the section and scroll to it
        header = self.browser.scroll_widget.section_headers.get(section)
        if header:
            self.browser.scroll_widget.scroll_area.ensureWidgetVisible(header)
