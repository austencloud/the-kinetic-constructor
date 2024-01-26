from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QSizePolicy, QHBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ..section_widget import SectionWidget
from PyQt6.QtCore import pyqtSignal


class SectionTypeLabel(QLabel):
    clicked = pyqtSignal()

    TYPE_MAP = {
        "Type1": "Dual-Shift",
        "Type2": "Shift",
        "Type3": "Cross-Shift",
        "Type4": "Dash",
        "Type5": "Dual-Dash",
        "Type6": "Static",
    }

    COLORS = {
        "Shift": "#6F2DA8",  # purple
        "Dual": "#00b3ff",  # cyan
        "Dash": "#26e600",  # green
        "Cross": "#26e600",  # green
        "Static": "#eb7d00",  # orange
        "-": "#000000",  # black
    }

    EXPAND_ARROW_PATH = "images/icons/dropdown/expand.png"
    COLLAPSE_ARROW_PATH = "images/icons/dropdown/collapse.png"

    def __init__(self, section_widget: "SectionWidget") -> None:
        super().__init__()
        self.section = section_widget
        self.arrow_label = QLabel()  # Additional label for the arrow icon

        # Load and resize the pixmaps
        self.expand_arrow_pixmap = self.load_and_resize_expand_pixmap(
            self.EXPAND_ARROW_PATH
        )
        self.collapse_arrow_pixmap = self.load_and_resize_collapse_pixmap(
            self.COLLAPSE_ARROW_PATH
        )

        self.toggle_dropdown_arrow(False)
        self.set_styled_text(section_widget.letter_type)

    def load_and_resize_collapse_pixmap(self, path: str) -> QPixmap:
        pixmap = QPixmap(path)
        # Resize pixmap to fit the label height
        collapse_height = (
            self.section.scroll_area.width() // 60
        )  # Example size, adjust as needed
        return pixmap.scaledToHeight(
            collapse_height, Qt.TransformationMode.SmoothTransformation
        )

    def load_and_resize_expand_pixmap(self, path: str) -> QPixmap:
        pixmap = QPixmap(path)
        # Resize pixmap to fit the label height
        collapse_height = (
            self.section.scroll_area.width() // 40
        )  # Example size, adjust as needed
        return pixmap.scaledToHeight(
            collapse_height, Qt.TransformationMode.SmoothTransformation
        )

    def set_styled_text(self, letter_type: str) -> None:
        type_words = self.TYPE_MAP.get(letter_type, "").split("-")

        styled_words = [
            f"<span style='color: {self.COLORS.get(word, 'black')};'>{word}</span>"
            for word in type_words
        ]

        styled_type_name = (
            "-".join(styled_words)
            if "-" in self.TYPE_MAP.get(letter_type, "")
            else "".join(styled_words)
        )

        styled_text = f"{letter_type[0:4]} {letter_type[4]}: {styled_type_name}"
        self.setText(styled_text)
        font_size = self.section.scroll_area.width() // 34
        self.setStyleSheet(f"font-size: {font_size}px; font-weight: bold;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )

    def toggle_dropdown_arrow(self, is_expanded) -> None:
        arrow_pixmap = (
            self.expand_arrow_pixmap if is_expanded else self.collapse_arrow_pixmap
        )
        self.arrow_label.setPixmap(arrow_pixmap)

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        self.clicked.emit()

