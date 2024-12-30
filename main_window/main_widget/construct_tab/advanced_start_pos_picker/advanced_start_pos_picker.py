from copy import deepcopy
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QSizePolicy
from typing import TYPE_CHECKING

from base_widgets.base_pictograph.base_pictograph import BasePictograph
from data.constants import BOX, DIAMOND
from main_window.main_widget.construct_tab.advanced_start_pos_picker.advanced_start_pos_picker_pictograph_view import (
    AdvancedStartPosPickerPictographView,
)
from main_window.main_widget.construct_tab.start_pos_picker.base_start_pos_picker import (
    BaseStartPosPicker,
)
from main_window.main_widget.construct_tab.start_pos_picker.choose_your_start_pos_label import (
    ChooseYourStartPosLabel,
)

if TYPE_CHECKING:
    from ..construct_tab import ConstructTab


class AdvancedStartPosPicker(BaseStartPosPicker):
    COLUMN_COUNT = 4

    def __init__(self, construct_tab: "ConstructTab"):
        super().__init__(construct_tab)
        self.choose_your_start_pos_label = ChooseYourStartPosLabel(self)
        self._setup_layout()
        self.start_pos_cache: dict[str, list[BasePictograph]] = {}
        self.start_position_adder = (
            self.construct_tab.main_widget.sequence_widget.beat_frame.start_position_adder
        )
        self.generate_variations()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()

        self.start_label_layout = QHBoxLayout()
        self.start_label_layout.addWidget(self.choose_your_start_pos_label)

        self.layout.addStretch(1)
        self.layout.addLayout(self.start_label_layout, 1)
        self.layout.addStretch(1)
        self.layout.addLayout(self.grid_layout, 15)
        self.layout.addStretch(1)

    def create_pictograph_from_dict(
        self, pictograph_dict: dict, target_grid_mode: str
    ) -> BasePictograph:
        pictograph_key = self.generate_pictograph_key(pictograph_dict, target_grid_mode)
        if pictograph_key in self.pictograph_cache:
            return self.pictograph_cache[pictograph_key]

        local_dict = deepcopy(pictograph_dict)
        local_dict["grid_mode"] = target_grid_mode

        pictograph = BasePictograph(self.main_widget)
        pictograph.view = AdvancedStartPosPickerPictographView(pictograph)
        pictograph.updater.update_pictograph(local_dict)
        pictograph.view.update_borders()

        self.pictograph_cache[pictograph_key] = pictograph

        # Also append to the parent's lists
        if target_grid_mode == BOX:
            self.box_pictographs.append(pictograph)
        elif target_grid_mode == DIAMOND:
            self.diamond_pictographs.append(pictograph)

        return pictograph

    def display_variations(self) -> None:
        # Clear the grid layout
        for i in reversed(range(self.grid_layout.count())):
            widget_to_remove = self.grid_layout.itemAt(i).widget()
            self.grid_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        # Add pictographs to the grid layout
        for _, variation_list in self.all_variations.items():
            for i, variation in enumerate(variation_list):
                row = i // self.COLUMN_COUNT
                col = i % self.COLUMN_COUNT
                self.grid_layout.addWidget(variation.view, row, col)
                self._resize_variation(variation)

    def generate_variations(self):
        self.all_variations: dict[str, list[BasePictograph]] = {BOX: [], DIAMOND: []}

        for grid_mode in [BOX, DIAMOND]:
            if grid_mode == BOX:
                variations = self.get_box_variations(advanced=True)
            else:
                variations = self.get_diamond_variations(advanced=True)

            for variation in variations:
                self.all_variations[grid_mode].append(variation)
                variation.view.mousePressEvent = (
                    lambda event, v=variation: self.on_variation_selected(v)
                )
                variation.view.update_borders()

    def _resize_variation(self, variation: BasePictograph) -> None:
        view_width = self.construct_tab.advanced_start_pos_picker.width() // 6
        variation.view.setFixedSize(view_width, view_width)
        variation.view.view_scale = view_width / variation.width()
        variation.view.resetTransform()
        variation.view.scale(variation.view.view_scale, variation.view.view_scale)

    def on_variation_selected(self, variation: BasePictograph) -> None:
        self.start_position_adder.add_start_pos_to_sequence(variation, True)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setVerticalSpacing(20)
        for _, variations in self.all_variations.items():
            for variation in variations:
                self._resize_variation(variation)
