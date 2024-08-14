from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QWidget, QScrollArea, QLabel
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, QPoint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class DictionaryNavSidebar(QWidget):
    def __init__(self, browser: "DictionaryBrowser"):
        super().__init__()
        self.browser = browser
        self._setup_scroll_area()
        self.buttons: list[QPushButton] = []
        self.year_labels: dict[str, QPushButton] = {}
        self.spacer_lines: list[QLabel] = []
        self.selected_button: QPushButton = None  # Track the selected button

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
        self._clear_sidebar()

        if sort_order == "date_added":
            self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            current_year = None
            for section in sections:
                if section == "Unknown":
                    continue
                year = section.split("-")[2]
                date = section
                day = self.get_formatted_day(date)

                if year != current_year:
                    year_label = QLabel(year)
                    year_label.setStyleSheet("font-weight: bold;")

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
            self.layout.setAlignment(Qt.AlignmentFlag(0))  # Remove alignment

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

        self._set_styles()

    def _clear_sidebar(self):
        for button in self.buttons:
            self.layout.removeWidget(button)
            button.deleteLater()
        for year_label in self.year_labels.values():
            self.layout.removeWidget(year_label)
            year_label.deleteLater()
        for spacer_line in self.spacer_lines:
            self.layout.removeWidget(spacer_line)
            spacer_line.deleteLater()
        self.buttons.clear()
        self.year_labels.clear()
        self.spacer_lines.clear()
        self.selected_button = None

    def get_formatted_day(self, date):
        day = date.split("-")[0].lstrip("0") + "-" + date.split("-")[1].lstrip("0")
        return day

    def style_button(self, button: QPushButton, selected: bool = False):
        font_size = self.browser.height() // 40
        if selected:
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: #333;
                    color: white;
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
                    color: #333;
                    padding: 5px;
                    text-align: center;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: #f0f0f0;
                }}
            """
            )

    def style_year_label(self, label: QLabel):
        font_size = self.browser.height() // 35
        label.setStyleSheet(
            f"""
            QLabel {{
                font-size: {font_size}px;
                color: #333;
                padding: 5px;
                text-align: center;
                font-weight: bold;
            }}
        """
        )

    def scroll_to_section(self, section, button: QPushButton):
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

    def _set_styles(self):
        for button in self.buttons:
            selected = button == self.selected_button
            self.style_button(button, selected=selected)
        for year_label in self.year_labels.values():
            self.style_year_label(year_label)
        for spacer_line in self.spacer_lines:
            spacer_line.setFixedHeight(1)

    def resizeEvent(self, event):
        self._set_styles()
        super().resizeEvent(event)
