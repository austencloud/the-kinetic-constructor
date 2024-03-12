from ast import List
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout
from typing import TYPE_CHECKING
from Enums.letters import Letter

from widgets.sequence_builder.components.start_pos_picker.start_pos_default_ori_picker import (
    StartPosDefaultOriPicker,
)


if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from ..sequence_builder import SequenceBuilder


class AdvancedStartPosPicker(QWidget):
    def __init__(self, sequence_builder: "SequenceBuilder"):
        super().__init__(sequence_builder)
        self.sequence_builder = sequence_builder
        self.main_widget = sequence_builder.main_widget
        self.start_pos_picker = self.sequence_builder.start_pos_picker
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)
        self.default_ori_picker = StartPosDefaultOriPicker(self)
        self.default_ori_picker.load_default_orientations()

    def display_variations(self, variations: list["Pictograph"]) -> None:
        self.view_width = self.calculate_view_width()
        alpha_variations = []
        beta_variations = []
        gamma_variations = []

        for variation in variations:
            if variation.letter == Letter.α:
                alpha_variations.append(variation)
            elif variation.letter == Letter.β:
                beta_variations.append(variation)
            elif variation.letter == Letter.Γ:
                gamma_variations.append(variation)

        all_variations: list["Pictograph"] = (
            alpha_variations + beta_variations + gamma_variations
        )

        for i, variation in enumerate(all_variations):
            row = i // 4
            col = i % 4
            self.grid_layout.addWidget(variation.view, row, col)
            variation.view.mousePressEvent = (
                lambda event, v=variation: self.on_variation_selected(v)
            )
            self._resize_variation(variation)
            variation.container.update_borders()

    def calculate_view_width(self) -> int:
        max_variations_per_row = 4
        view_width = self.sequence_builder.height() // 5
        return view_width

    def init_ui(self):
        variations = self.start_pos_picker.start_pos_manager.get_all_start_positions()
        self.display_variations(variations)

    def _resize_variation(self, variation: "Pictograph") -> None:
        variation.view.setFixedSize(self.view_width, self.view_width)
        variation.view.view_scale = self.view_width / variation.view.pictograph.width()
        variation.view.resetTransform()
        variation.view.scale(variation.view.view_scale, variation.view.view_scale)
        variation.container.styled_border_overlay.setFixedSize(
            variation.view.width(), variation.view.height()
        )
        variation.container.styled_border_overlay.setFixedSize(
            variation.view.width(), variation.view.height()
        )

    def on_variation_selected(self, variation: "Pictograph") -> None:
        self.sequence_builder.start_pos_picker.start_pos_manager.on_start_pos_clicked(
            variation
        )

    def select_variation(self, variation):
        self.sequence_builder.set_selected_start_position(variation)
        self.sequence_builder.transition_to_sequence_building()

    def show_variations(self):
        self.sequence_builder.simple_start_pos_picker.hide()
        self.show()
