# codex_widget.py

from typing import TYPE_CHECKING, Dict, Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGridLayout,
    QScrollArea,
    QLabel,
    QComboBox,
    QSizePolicy,
)
from PyQt6.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    QSize,
)
from PyQt6.QtGui import QFont

from Enums.letters import LetterType
from main_window.main_widget.learn_widget.codex_widget.placeholder_pictograph import (
    PlaceholderPictograph,
)

if TYPE_CHECKING:
    from base_widgets.base_pictograph.pictograph_view import PictographView
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget


# Define the sections for the Codex
SECTIONS_PART1 = [
    [
        ["A", "B", "C", "D", "E", "F"],
        ["G", "H", "I", "J", "K", "L"],
        ["M", "N", "O", "P", "Q", "R"],
        ["S", "T", "U", "V"],
    ],
    [["W", "X", "Y", "Z"], ["Σ", "Δ", "θ", "Ω"]],
]

SECTIONS_PART2 = [
    [["W-", "X-", "Y-", "Z-"], ["Σ-", "Δ-", "θ-", "Ω-"]],
    [["Φ", "Ψ", "Λ"]],
    [["Φ-", "Ψ-", "Λ-"]],
    [["α", "β", "Γ"]],
]

TYPE_MAP = {
    LetterType.Type1: "Dual-Shift",
    LetterType.Type2: "Shift",
    LetterType.Type3: "Cross-Shift",
    LetterType.Type4: "Dash",
    LetterType.Type5: "Dual-Dash",
    LetterType.Type6: "Static",
}


class CodexWidget(QWidget):
    """Widget to display the codex with all pictographs organized into sections."""

    def __init__(
        self, learn_widget: "LearnWidget", pictograph_data: Dict[str, Optional[dict]]
    ):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget
        self.pictograph_data = pictograph_data

        self.setMinimumWidth(0)
        self.setMaximumWidth(int(self.learn_widget.width() * 0.5))  # Max width at 50%
        self.setFixedWidth(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(
            # make it transparent
            "background-color: rgba(255, 255, 255, 0);"
        )
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Top bar with global modifications
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        self.rotate_btn = QPushButton("Rotate")
        self.rotate_btn.clicked.connect(self.rotate_all)
        self.mirror_btn = QPushButton("Mirror")
        self.mirror_btn.clicked.connect(self.mirror_all)
        self.color_swap_btn = QPushButton("Color Swap")
        self.color_swap_btn.clicked.connect(self.color_swap_all)

        self.orientation_selector = QComboBox()
        self.orientation_selector.addItems(["in", "out"])  # Example orientations
        self.orientation_selector.currentTextChanged.connect(
            self.update_orientation_all
        )

        top_bar.addWidget(self.rotate_btn)
        top_bar.addWidget(self.mirror_btn)
        top_bar.addWidget(self.color_swap_btn)
        top_bar.addWidget(QLabel("Orientation:"))
        top_bar.addWidget(self.orientation_selector)
        top_bar.addStretch()
        self.main_layout.addLayout(top_bar)

        # Scrollable area for pictographs
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        self.main_vlayout = QVBoxLayout(content_widget)
        self.main_vlayout.setContentsMargins(0, 0, 0, 0)
        self.main_vlayout.setSpacing(0)

        self.letter_views: Dict[str, "PictographView"] = {}

        # Load all sections
        self.load_section_with_label(SECTIONS_PART1)
        self.load_section_with_label(SECTIONS_PART2)

        scroll.setWidget(content_widget)
        self.main_layout.addWidget(scroll)

        # Animation for showing/hiding codex
        self.animation = QPropertyAnimation(self, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)

    def load_section_with_label(self, sections):
        """
        Loads a major section of the codex (like PART1 or PART2) and determines
        the letter type from the first letter in this section to display a heading label.
        """
        from base_widgets.base_pictograph.base_pictograph import BasePictograph
        from base_widgets.base_pictograph.pictograph_view import PictographView

        # Determine letter type from the first letter in the first subgroup
        first_letter = sections[0][0][0]  # First letter of the first row
        pictograph_dict = self.pictograph_data.get(first_letter, None)
        if pictograph_dict and "letter_type" in pictograph_dict:
            try:
                letter_type_enum = LetterType[pictograph_dict["letter_type"]]
                type_label_str = f"Type {letter_type_enum.value}: {TYPE_MAP.get(letter_type_enum, 'Unknown Type')}"
            except KeyError:
                type_label_str = "Type Unknown: Unknown Type"
        else:
            type_label_str = "Type Unknown: Unknown Type"

        # Add a label for this type
        type_label = QLabel()
        type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        font = QFont()
        font.setBold(True)
        type_label.setFont(font)
        type_label.setText(type_label_str)
        self.main_vlayout.addWidget(type_label)

        # Now load all letters in a QGridLayout
        grid = QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        row_counter = 0
        for section in sections:
            for row_letters in section:
                col_counter = 0
                for letter_str in row_letters:
                    p_dict = self.pictograph_data.get(letter_str, None)
                    if p_dict:
                        # Assuming BasePictograph is initialized with necessary parameters
                        scene = BasePictograph(self.main_widget)
                        scene.updater.update_pictograph(p_dict)

                        view = PictographView(scene)
                        self.letter_views[letter_str] = view
                        grid.addWidget(view, row_counter, col_counter)
                    else:
                        print(
                            f"Pictograph data for letter '{letter_str}' is incomplete or missing. Using placeholder."
                        )
                        scene = PlaceholderPictograph(self.main_widget)
                        view = PictographView(scene)
                        self.letter_views[letter_str] = view
                        grid.addWidget(view, row_counter, col_counter)
                    col_counter += 1
                row_counter += 1

        self.main_vlayout.addLayout(grid)

    def toggle_codex(self, show: bool):
        """
        Animate the codex panel to show or hide.
        """
        end_val = int(self.learn_widget.width() * 0.5) if show else 0
        self.animation.stop()
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(end_val)
        self.animation.finished.connect(lambda: self.setFixedWidth(end_val))
        self.animation.start()

    # Global modifications (placeholders)
    def rotate_all(self):
        sequence_rotation_manager = self.main_widget.sequence_widget.rotation_manager
        for letter_str, view in self.letter_views.items():
            scene = view.pictograph
            if scene.pictograph_dict:
                rotated_pictograph_dict = scene.pictograph_dict.copy()
                sequence_rotation_manager.rotate_pictograph(rotated_pictograph_dict, 1)
                scene.updater.update_pictograph(rotated_pictograph_dict)

    def mirror_all(self):
        for letter_str, view in self.letter_views.items():
            scene = view.pictograph
            if scene.pictograph_dict:
                # Implement actual mirror logic here
                # Placeholder: just re-update the same dict
                scene.updater.update_pictograph(scene.pictograph_dict)

    def color_swap_all(self):
        for letter_str, view in self.letter_views.items():
            scene = view.pictograph
            if scene.pictograph_dict:
                # Implement actual color swap logic here
                # Placeholder: just re-update the same dict
                scene.updater.update_pictograph(scene.pictograph_dict)

    def update_orientation_all(self, orientation: str):
        for letter_str, view in self.letter_views.items():
            scene = view.pictograph
            if scene.pictograph_dict:
                new_dict = scene.pictograph_dict.copy()
                if "blue_attributes" in new_dict:
                    new_dict["blue_attributes"]["start_ori"] = orientation
                if "red_attributes" in new_dict:
                    new_dict["red_attributes"]["start_ori"] = orientation
                scene.updater.update_pictograph(new_dict)

    def resizeEvent(self, event):
        """Override resizeEvent to adjust pictograph sizes dynamically."""
        super().resizeEvent(event)
        self.adjust_pictograph_sizes()

    def adjust_pictograph_sizes(self):
        """Adjust the size of all pictographs to be square based on codex width."""
        codex_width = (
            self.width()
            - self.main_vlayout.contentsMargins().left()
            - self.main_vlayout.contentsMargins().right()
        )
        square_size = codex_width // 6  # Divide by 6 as per requirement

        for view in self.letter_views.values():
            view.setFixedSize(QSize(square_size, square_size))
