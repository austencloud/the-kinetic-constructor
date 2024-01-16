from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtWidgets import (
    QScrollArea,
    QWidget,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QTimer
from Enums import LetterNumberType
from utilities.TypeChecking.TypeChecking import Letters
from widgets.ig_tab.ig_scroll.ig_pictograph import IGPictograph
from .scroll_area_display_manager import ScrollAreaDisplayManager
from .scroll_area_filter_manager import ScrollAreaFilterFrameManager
from .scroll_area_pictograph_factory import ScrollAreaPictographFactory

if TYPE_CHECKING:
    from ..main_widget import MainWidget


class PictographScrollArea(QScrollArea):
    def __init__(self, main_widget: "MainWidget", parent_tab) -> None:
        super().__init__(parent_tab)
        self.main_widget = main_widget
        self.parent_tab = parent_tab
        self.letters = self.main_widget.letters
        self.pictographs: Dict[Letters, IGPictograph] = {}
        self.pictograph_factory = ScrollAreaPictographFactory(self)
        self.display_manager = ScrollAreaDisplayManager(self)
        self.filter_frame_manager = ScrollAreaFilterFrameManager(self)
        self.sections: Dict[str, QGridLayout] = {}
        self.letters_by_type: Dict[str, List[str]] = self.setup_letters_by_type()
        self._setup_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_arrow_placements)
        self.timer.start(1000)

    def setup_letters_by_type(self) -> Dict[str, List[str]]:
        letters_by_type = {}
        for letter_type in LetterNumberType:
            letters_by_type[letter_type.description] = letter_type.letters
        return letters_by_type

    def _setup_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.container.setContentsMargins(10, 10, 10, 10)
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def get_pictograph_letter_type(self, pictograph_key: str) -> str:
        letter = pictograph_key.split("_")[0]
        for letter_type, letters in self.letters_by_type.items():
            if letter in letters:
                return letter_type
        return "Unknown"

    def organize_pictographs_by_type(self) -> None:
        self.clear_sections()
        pictographs_by_type = {type: [] for type in self.letters_by_type.keys()}
        for key, pictograph in self.pictographs.items():
            letter_type = self.get_pictograph_letter_type(key)
            pictographs_by_type[letter_type].append(pictograph)

        for letter_type, pictographs in pictographs_by_type.items():
            self.create_section(letter_type)
            for index, pictograph in enumerate(pictographs):
                self.display_manager.add_pictograph_to_layout(pictograph, index)

    def update_pictographs(self) -> None:
        deselected_letters = self.pictograph_factory.get_deselected_letters()
        for letter in deselected_letters:
            self.pictograph_factory.remove_deselected_letter_pictographs(letter)
        self.pictograph_factory.process_selected_letters()
        self.display_manager.cleanup_unused_pictographs()
        self.filter_frame_manager.update_filter_frame_if_needed()
        self.organize_pictographs_by_type()

    def clear_sections(self) -> None:
        """Clears all sections from the layout."""
        while self.layout.count():
            layout_item = self.layout.takeAt(0)
            if layout_item.widget():
                layout_item.widget().hide()
        self.sections.clear()

    # In PictographScrollArea class

    def create_section(self, letter_type: str) -> None:
        """Creates a new section for a given letter type."""
        section_frame = QWidget()
        section_layout = QGridLayout(section_frame)
        type_map = {
            "Type1": "Dual-Shifts",
            "Type2": "Shifts",
            "Type3": "Cross-Shifts",
            "Type4": "Dashes",
            "Type5": "Dual-Dashes",
            "Type6": "Statics",
        }

        colors = {
            "Shift": "#800080",  # purple
            "Shifts": "#800080",  # purple
            "Dual": "#008080",  # teal
            "Dash": "#008000",  # green
            "Dashes": "#008000",  # green
            "Cross": "#008000",  # green
            "Statics": "#FFA500",  # orange
            "-": "black",  # Assuming you want the hyphen in 'Dual-Dash
        }

        # Extract the words from type_name for styling
        type_words = type_map[letter_type].split("-")

        # Apply HTML styling to each word based on its meaning
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
        section_label = QLabel()
        section_label.setText(styled_text)  # Set the HTML styled text
        font_size = self.calculate_font_size()

        section_label.setStyleSheet(f"font-size: {font_size}px; font-weight: bold;")

        size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        section_label.setSizePolicy(size_policy)

        section_label.setMinimumSize(section_label.sizeHint())

        section_layout.addWidget(
            section_label, 0, 0, 1, self.display_manager.COLUMN_COUNT
        )
        self.layout.addWidget(section_frame)
        self.sections[letter_type] = section_layout

    def calculate_font_size(self) -> int:
        # Calculate the font size relative to the window size
        window_width = self.width()
        font_size = window_width // 50  # Adjust the division factor as needed
        return font_size

    def update_arrow_placements(self) -> None:
        for pictograph in self.pictographs.values():
            pictograph.arrow_placement_manager.update_arrow_placement()
