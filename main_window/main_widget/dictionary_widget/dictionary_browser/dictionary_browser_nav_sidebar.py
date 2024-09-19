from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QApplication
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class DictionaryBrowserNavSidebar(QWidget):
    def __init__(self, browser: "DictionaryBrowser"):
        super().__init__()
        self.browser = browser
        self._setup_scroll_area()
        self.buttons: list[QPushButton] = []
        self.year_labels: dict[str, QPushButton] = {}
        self.spacer_lines: list[QLabel] = []
        self.length_label: QLabel = None  # New attribute for the length label
        self.length_spacer_line: QLabel = None  # Spacer line for length label
        self.letter_label: QLabel = None  # New attribute for the letter label
        self.letter_spacer_line: QLabel = None  # Spacer line for letter label
        self.selected_button: QPushButton = None  # Track the selected button
        self.settings_manager = (
            self.browser.dictionary_widget.main_widget.main_window.settings_manager
        )

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

    def _setup_scroll_area(self):
        self.scroll_content = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout(self.scroll_content)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_content.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setStyleSheet("background: transparent;")

    def update_sidebar(self, sections, sort_order):
        self.clear_sidebar()

        if sort_order == "sequence_length":
            self.layout.setAlignment(
                Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignVCenter
            )

            # Create and style the length label
            self.length_label = QLabel("Length")
            self.style_header_label(self.length_label)
            self.layout.addWidget(self.length_label)

            # Add a spacer line below the length label
            self.length_spacer_line = QLabel()
            self.length_spacer_line.setStyleSheet(
                "border: 1px solid black; margin: 0px 0; background: black;"
            )
            self.layout.addWidget(self.length_spacer_line)

            # Add buttons for each section (sequence length)
            for section in sections:
                button = QPushButton(str(section))
                button.clicked.connect(
                    lambda checked, sec=section, btn=button: self.scroll_to_section(
                        sec, btn
                    )
                )
                button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.layout.addWidget(button)
                self.buttons.append(button)

        elif sort_order == "alphabetical":
            self.layout.setAlignment(
                Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignVCenter
            )

            # Create and style the letter label
            self.letter_label = QLabel("Letter")
            self.style_header_label(self.letter_label)
            self.layout.addWidget(self.letter_label)

            # Add a spacer line below the letter label
            self.letter_spacer_line = QLabel()
            self.letter_spacer_line.setStyleSheet(
                "border: 1px solid black; margin: 0px 0; background: black;"
            )
            self.layout.addWidget(self.letter_spacer_line)

            # Add buttons for each section (letters)
            for section in sections:
                button = QPushButton(str(section))
                button.clicked.connect(
                    lambda checked, sec=section, btn=button: self.scroll_to_section(
                        sec, btn
                    )
                )
                button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.layout.addWidget(button)
                self.buttons.append(button)

        elif sort_order == "date_added":
            self.layout.setAlignment(
                Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignVCenter
            )

            current_year = None
            for section in sections:
                if section == "Unknown":
                    continue
                year = section.split("-")[2]
                date = section
                day = self.get_formatted_day(date)

                if year != current_year:
                    year_label = QLabel(year)
                    year_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.style_header_label(year_label)
                    self.layout.addWidget(year_label)
                    spacer_line = QLabel()
                    spacer_line.setStyleSheet(
                        "border: 1px solid black; margin: 0px 0; background: black;"
                    )
                    self.spacer_lines.append(spacer_line)
                    self.layout.addWidget(spacer_line)

                    self.year_labels[year] = year_label
                    current_year = year

                date_button = QPushButton(day)
                date_button.clicked.connect(
                    lambda checked, sec=section, btn=date_button: self.scroll_to_section(
                        sec, btn
                    )
                )
                date_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.layout.addWidget(date_button)
                self.buttons.append(date_button)

        else:
            self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            for section in sections:
                button = QPushButton(str(section))
                button.clicked.connect(
                    lambda checked, sec=section, btn=button: self.scroll_to_section(
                        sec, btn
                    )
                )
                button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                self.layout.addWidget(button)
                self.buttons.append(button)

        self.set_styles()

    def clear_sidebar(self):
        for button in self.buttons:
            self.layout.removeWidget(button)
            button.hide()
            button.deleteLater()
        for year_label in self.year_labels.values():
            self.layout.removeWidget(year_label)
            year_label.hide()
            year_label.deleteLater()
        for spacer_line in self.spacer_lines:
            self.layout.removeWidget(spacer_line)
            spacer_line.hide()
            spacer_line.deleteLater()

        # Clear the length label and its spacer if they exist
        if self.length_label:
            self.layout.removeWidget(self.length_label)
            self.length_label.hide()
            self.length_label.deleteLater()
            self.length_label = None
        if self.length_spacer_line:
            self.layout.removeWidget(self.length_spacer_line)
            self.length_spacer_line.hide()
            self.length_spacer_line.deleteLater()
            self.length_spacer_line = None

        # Clear the letter label and its spacer if they exist
        if self.letter_label:
            self.layout.removeWidget(self.letter_label)
            self.letter_label.hide()
            self.letter_label.deleteLater()
            self.letter_label = None
        if self.letter_spacer_line:
            self.layout.removeWidget(self.letter_spacer_line)
            self.letter_spacer_line.hide()
            self.letter_spacer_line.deleteLater()
            self.letter_spacer_line = None

        self.buttons.clear()
        self.year_labels.clear()
        self.spacer_lines.clear()
        self.selected_button = None
        QApplication.processEvents()

    def get_formatted_day(self, date: str) -> str:
        day = date.split("-")[0].lstrip("0") + "-" + date.split("-")[1].lstrip("0")
        return day

    def style_button(self, button: QPushButton, selected: bool = False):
        font_size = self.browser.height() // 40
        font_color = self.settings_manager.global_settings.font_color_updater.get_font_color(
            self.settings_manager.global_settings.get_background_type()
        )
        button_background_color = "lightgray" if font_color == "black" else "#555"
        hover_color = "lightgray" if font_color == "black" else "#555"
        if selected:
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {button_background_color};
                    color: {font_color};
                    border-radius: 5px;
                    font-size: {font_size}px;
                    padding: 5px;
                    font-weight: bold;
                }}
                """
            )
        else:
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    font-size: {font_size}px;
                    color: {font_color};
                    padding: 5px;
                    text-align: center;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: {hover_color};
                }}
            """
            )

    def style_header_label(self, label: QLabel):
        font_size = self.browser.height() // 40
        font_color = self.settings_manager.global_settings.font_color_updater.get_font_color(
            self.settings_manager.global_settings.get_background_type()
        )
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            f"""
            QLabel {{
                font-size: {font_size}px;
                color: {font_color};
                padding: 5px;
                font-weight: bold;
            }}
        """
        )

    def scroll_to_section(self, section: str, button: QPushButton):
        if self.selected_button:
            self.style_button(self.selected_button, selected=False)
        self.style_button(button, selected=True)
        self.selected_button = button

        if "-" in section:
            section = (
                section.split("-")[0].lstrip("0")
                + "-"
                + section.split("-")[1].lstrip("0")
            )
        header = self.browser.scroll_widget.section_headers.get(section)
        if header:
            scroll_area = self.browser.scroll_widget.scroll_area
            header_global_pos = header.mapToGlobal(QPoint(0, 0))
            content_widget_pos = scroll_area.widget().mapFromGlobal(header_global_pos)
            vertical_pos = content_widget_pos.y()
            scroll_area.verticalScrollBar().setValue(vertical_pos)

    def set_styles(self):
        for button in self.buttons:
            selected = button == self.selected_button
            self.style_button(button, selected=selected)
        for year_label in self.year_labels.values():
            self.style_header_label(year_label)
        for spacer_line in self.spacer_lines:
            spacer_line.setFixedHeight(1)
        if self.length_label:
            self.style_header_label(self.length_label)
        if self.length_spacer_line:
            self.length_spacer_line.setFixedHeight(1)
        if self.letter_label:
            self.style_header_label(self.letter_label)
        if self.letter_spacer_line:
            self.letter_spacer_line.setFixedHeight(1)

    def resize_nav_sidebar(self):
        self.set_styles()
