# codex_widget.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QGridLayout,
    QScrollArea,
    QLabel,
    QComboBox,
)
from PyQt6.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    pyqtSignal,
    QRect,
    QParallelAnimationGroup,
)
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Dict


if TYPE_CHECKING:
    from base_widgets.base_pictograph.bordered_pictograph_view import (
        BorderedPictographView,
    )
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget
    from base_widgets.base_pictograph.base_pictograph import BasePictograph

SECTIONS = [
    [
        ["A", "B", "C", "D", "E", "F"],
        ["G", "H", "I", "J", "K", "L"],
        ["M", "N", "O", "P", "Q", "R"],
        ["S", "T", "U", "V"],
    ],
    [["W", "X", "Y", "Z"], ["Σ", "Δ", "θ", "Ω"]],
    [["W-", "X-", "Y-", "Z-"], ["Σ-", "Δ-", "θ-", "Ω-"]],
    [["Φ", "Ψ", "Λ"]],
    [["Φ-", "Ψ-", "Λ-"]],
    [["α", "β", "Γ"]],
]


class CodexWidget(QWidget):
    def __init__(self, learn_widget: "LearnWidget", pictograph_data: dict):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget
        self.pictograph_data = pictograph_data

        self.setMinimumWidth(0)
        self.setMaximumWidth(int(self.learn_widget.width() * 0.5))  # Max width at 50%
        self.setFixedWidth(0)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(5)

        # Top bar with global modifications
        top_bar = QHBoxLayout()
        self.rotate_btn = QPushButton("Rotate")
        self.rotate_btn.clicked.connect(self.rotate_all)
        self.mirror_btn = QPushButton("Mirror")
        self.mirror_btn.clicked.connect(self.mirror_all)
        self.color_swap_btn = QPushButton("Color Swap")
        self.color_swap_btn.clicked.connect(self.color_swap_all)

        self.orientation_selector = QComboBox()
        self.orientation_selector.addItems(["in", "out"])  # Example orientations
        self.orientation_selector.currentTextChanged.connect(self.update_orientation_all)

        top_bar.addWidget(self.rotate_btn)
        top_bar.addWidget(self.mirror_btn)
        top_bar.addWidget(self.color_swap_btn)
        top_bar.addWidget(QLabel("Orientation:"))
        top_bar.addWidget(self.orientation_selector)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # Scrollable area for pictographs
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        self.grid_layout = QVBoxLayout(content_widget)
        self.grid_layout.setContentsMargins(5,5,5,5)
        self.grid_layout.setSpacing(10)

        self.letter_views: dict[str, "BorderedPictographView"] = {}
        self.load_pictographs()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        self.animation = QPropertyAnimation(self, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)

    def load_pictographs(self):
        from base_widgets.base_pictograph.base_pictograph import BasePictograph
        from base_widgets.base_pictograph.bordered_pictograph_view import BorderedPictographView

        # Create a grid (QGridLayout) for sections
        # Replace self.grid_layout with a QGridLayout if you want a strict grid
        # For demonstration, use a QGridLayout for neat alignment:
        from PyQt6.QtWidgets import QGridLayout
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setContentsMargins(5,5,5,5)

        row_counter = 0
        for section in SECTIONS:
            for row_letters in section:
                col_counter = 0
                for letter_str in row_letters:
                    pictograph_dict = self.pictograph_data.get(letter_str, None)

                    pictograph_scene = BasePictograph(self.main_widget)
                    if pictograph_dict:
                        pictograph_scene.updater.update_pictograph(pictograph_dict)
                    view = BorderedPictographView(pictograph_scene)
                    self.letter_views[letter_str] = view
                    grid.addWidget(view, row_counter, col_counter)
                    col_counter += 1
                row_counter += 1

        self.grid_layout.addLayout(grid)

    def toggle_codex(self, show: bool):
        end_val = int(self.learn_widget.width()*0.5) if show else 0
        self.animation.stop()
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(end_val)
        self.animation.finished.connect(lambda: self.setFixedWidth(end_val))
        self.animation.start()

    # Global modifications (placeholders)
    def rotate_all(self):
        # Integrate actual rotation logic or leave as-is for now
        for letter_str, view in self.letter_views.items():
            scene = view.pictograph
            if scene.pictograph_dict:
                # Placeholder: just re-update the same dict
                scene.updater.update_pictograph(scene.pictograph_dict)

    def mirror_all(self):
        for letter_str, view in self.letter_views.items():
            scene = view.pictograph
            if scene.pictograph_dict:
                scene.updater.update_pictograph(scene.pictograph_dict)

    def color_swap_all(self):
        for letter_str, view in self.letter_views.items():
            scene = view.pictograph
            if scene.pictograph_dict:
                scene.updater.update_pictograph(scene.pictograph_dict)

    def update_orientation_all(self, orientation: str):
        for letter_str, view in self.letter_views.items():
            scene = view.pictograph
            if scene.pictograph_dict:
                new_dict = scene.pictograph_dict
                if "blue_attributes" in new_dict:
                    new_dict["blue_attributes"]["start_ori"] = orientation
                if "red_attributes" in new_dict:
                    new_dict["red_attributes"]["start_ori"] = orientation
                scene.updater.update_pictograph(new_dict)

