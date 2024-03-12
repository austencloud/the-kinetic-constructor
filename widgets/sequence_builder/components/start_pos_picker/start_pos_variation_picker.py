from PyQt6.QtWidgets import QWidget, QGridLayout

from ....pictograph.pictograph import Pictograph
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.sequence_builder.components.start_position_picker.start_pos_variation_dialog import (
        StartPosVariationDialog,
    )


class StartPosVariationPicker(QWidget):
    def __init__(self, variation_dialog: "StartPosVariationDialog"):
        super().__init__(variation_dialog)
        self.variation_dialog = variation_dialog
        self.layout: QGridLayout = QGridLayout(self)
        self.selected_variation: Pictograph = None

    def display_variations(self, variations: list[Pictograph]) -> None:
        self.clear_layout()
        self.view_width = self.calculate_view_width()
        for i, variation in enumerate(variations):
            row = i // 4
            col = i % 4
            self.layout.addWidget(variation.view, row, col)
            variation.view.mousePressEvent = (
                lambda event, v=variation: self.on_variation_clicked(v)
            )
            self._resize_variation(variation)
            variation.container.update_borders()

    def _resize_variation(self, variation: Pictograph) -> None:
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

    def calculate_view_width(self) -> int:
        dialog_width = self.variation_dialog.width()
        dialog_height = self.variation_dialog.height()
        max_variations_per_row = 4
        view_width = min(dialog_width // max_variations_per_row, dialog_height // 3)
        return view_width

    def clear_layout(self) -> None:
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

    def on_variation_clicked(self, variation: Pictograph) -> None:
        self.selected_variation = variation
        self.variation_dialog.accept()

    def get_selected_variation(self) -> Pictograph:
        return self.selected_variation
