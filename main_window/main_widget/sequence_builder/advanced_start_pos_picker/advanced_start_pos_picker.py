from PyQt6.QtWidgets import QGridLayout, QVBoxLayout
from typing import TYPE_CHECKING
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from data.constants import BOX
from main_window.main_widget.sequence_builder.components.start_pos_picker.base_start_pos_picker import (
    BaseStartPosPicker,
)
from main_window.main_widget.sequence_builder.components.start_pos_picker.choose_your_start_pos_label import (
    ChooseYourStartPosLabel,
)

if TYPE_CHECKING:
    from ..manual_builder import ManualBuilderWidget


class AdvancedStartPosPicker(BaseStartPosPicker):
    def __init__(self, manual_builder: "ManualBuilderWidget"):
        super().__init__(manual_builder)
        self.choose_your_start_pos_label = ChooseYourStartPosLabel(self)
        self._setup_layout()
        self.start_pos_cache: dict[str, list[BasePictograph]] = {}

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()
        self.layout.addStretch(1)
        self.layout.addWidget(self.choose_your_start_pos_label)
        self.layout.addStretch(1)
        self.layout.addLayout(self.grid_layout)
        self.layout.addStretch(1)

    def display_variations(self, grid_mode:str) -> None:
        if grid_mode == BOX:
            variations = self.get_box_variations()
        else:
            variations = self.get_diamond_variations()

        # Organize variations by letter
        letters = ["α", "β", "Γ"]
        self.start_pos_cache = {letter: [] for letter in letters}

        for variation in variations:
            self.start_pos_cache[variation.letter.value].append(variation)

        self.all_variations: list["BasePictograph"] = []
        for letter in letters:
            self.all_variations.extend(self.start_pos_cache[letter])

        # Clear the grid layout first
        for i in reversed(range(self.grid_layout.count())):
            widget_to_remove = self.grid_layout.itemAt(i).widget()
            self.grid_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        # Add variations to the grid layout
        for i, variation in enumerate(self.all_variations):
            row = i // 4
            col = i % 4
            self.grid_layout.addWidget(variation.view, row, col)
            variation.view.mousePressEvent = (
                lambda event, v=variation: self.on_variation_selected(v)
            )
            self._resize_variation(variation)
            variation.container.update_borders()

    def _resize_variation(self, variation: "BasePictograph") -> None:
        view_width = int(self.manual_builder.height() // 6)
        variation.view.setFixedSize(view_width, view_width)
        variation.view.view_scale = view_width / variation.view.pictograph.width()
        variation.view.resetTransform()
        variation.view.scale(variation.view.view_scale, variation.view.view_scale)
        variation.container.styled_border_overlay.setFixedSize(
            variation.view.width(), variation.view.height()
        )

    def on_variation_selected(self, variation: "BasePictograph") -> None:
        # Use the cached pictograph
        self.manual_builder.start_pos_picker.add_start_pos_to_sequence(variation)

    def resize_advanced_start_pos_picker(self) -> None:
        self.choose_your_start_pos_label.set_stylesheet()
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setVerticalSpacing(20)

