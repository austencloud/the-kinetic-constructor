# Import necessary components
from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QLabel,
    QSizePolicy,
)

from utilities.TypeChecking.TypeChecking import LetterTypeNums
from widgets.filter_tab import FilterTab
from ..ig_tab.ig_pictograph import IGPictograph

if TYPE_CHECKING:
    from .scroll_area import ScrollArea


class ScrollAreaSection(QWidget):
    def __init__(
        self,
        letter_type: LetterTypeNums,
        filter_tab,
        scroll_area: "ScrollArea",
    ) -> None:
        super().__init__(scroll_area)
        self.scroll_area = scroll_area
        self.letter_type = letter_type
        self.filter_tab: FilterTab = filter_tab
        self.pictographs: List[IGPictograph] = []
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.pictograph_frame = QFrame()
        self.pictograph_layout: QGridLayout = QGridLayout(self.pictograph_frame)
        self.styled_text = self.get_styled_text(letter_type)
        self.section_label = self.create_section_label(self.styled_text)
        self.initialize_ui()

    def create_section_label(self, styled_text: str) -> QLabel:
        """Creates a QLabel for the section label with the given styled text."""
        section_label = QLabel()
        section_label.setText(styled_text)  # Set the HTML styled text
        font_size = 25
        section_label.setStyleSheet(f"font-size: {font_size}px; font-weight: bold;")
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        section_label.setSizePolicy(size_policy)
        section_label.setMinimumSize(section_label.sizeHint())
        return section_label

    def initialize_ui(self) -> None:
        self.layout.addWidget(self.section_label)
        self.layout.addWidget(self.filter_tab)
        self.layout.addWidget(self.pictograph_frame)

    def add_pictograph(self, pictograph: IGPictograph) -> None:
        self.pictograph_layout.addWidget(pictograph.view)

    def remove_pictograph(self, pictograph: IGPictograph) -> None:
        # pictograph.view.hide()
        pictograph.view.setParent(None)
        # pictograph.setParent(None)

    def update_filter(self) -> None:
        pass

    def get_styled_text(self, letter_type: LetterTypeNums) -> str:
        """Returns the styled text for the section label."""
        type_map = {
            "Type1": "Dual-Shift",
            "Type2": "Shift",
            "Type3": "Cross-Shift",
            "Type4": "Dash",
            "Type5": "Dual-Dash",
            "Type6": "Static",
        }

        colors = {
            "Shift": "#6F2DA8",  # purple
            "Dual": "#00b3ff",  # cyan
            "Dash": "#26e600",  # green
            "Cross": "#26e600",  # green
            "Static": "#ff4000",  # orange
            "-": "#000000",  # black
        }

        type_words = type_map[letter_type].split("-")

        styled_words = []
        for word in type_words:
            color = colors.get(word, "black")
            styled_words.append(f"<span style='color: {color};'>{word}</span>")

        styled_type_name = (
            "-".join(styled_words)
            if "-" in type_map[letter_type]
            else "".join(styled_words)
        )

        styled_text = f"{letter_type[0:4]} {letter_type[4]}: {styled_type_name}"
        return styled_text

    def resize_scroll_area_section(self) -> None:
        self.section_label.setMinimumSize(self.section_label.sizeHint())
        self.section_label.setMaximumSize(self.section_label.sizeHint())
        self.filter_tab.resize_filter_tab()
