from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout
from typing import TYPE_CHECKING
from Enums.letters import Letter
from main_window.main_widget.top_builder_widget.sequence_builder.advanced_start_pos_picker.advanced_start_pos_ori_picker import (
    AdvancedStartPosOriPicker,
)
from main_window.main_widget.top_builder_widget.sequence_builder.advanced_start_pos_picker.advanced_start_pos_picker_pictograph_factory import (
    AdvancedStartPosPickerPictographFactory,
)
from main_window.main_widget.top_builder_widget.sequence_builder.components.start_pos_picker.advanced_start_pos_manager import (
    AdvancedStartPosManager,
)
from main_window.main_widget.top_builder_widget.sequence_builder.components.start_pos_picker.advanced_start_pos_picker_pictograph_frame import (
    AdvancedStartPosPickerPictographFrame,
)
from main_window.main_widget.top_builder_widget.sequence_builder.components.start_pos_picker.choose_your_start_pos_label import (
    ChooseYourStartPosLabel,
)


if TYPE_CHECKING:
    from widgets.base_widgets.pictograph.pictograph import BasePictograph

    from ..sequence_builder import SequenceBuilder


class AdvancedStartPosPicker(QWidget):
    def __init__(self, sequence_builder: "SequenceBuilder"):
        super().__init__(sequence_builder)
        self.sequence_builder = sequence_builder
        self.main_widget = sequence_builder.main_widget
        self.start_pos_picker = self.sequence_builder.start_pos_picker
        self.start_pos_cache: dict[str, list[BasePictograph]] = {}
        self.ori_picker = AdvancedStartPosOriPicker(self)
        self.pictograph_frame = AdvancedStartPosPickerPictographFrame(self)
        self.choose_you_start_pos_label = ChooseYourStartPosLabel(self)
        self.pictograph_factory = AdvancedStartPosPickerPictographFactory(
            self, self.start_pos_cache
        )
        self.advanced_start_pos_manager = AdvancedStartPosManager(self)
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()
        self.layout.addWidget(self.ori_picker, 1)
        self.layout.addLayout(self.grid_layout, 16)

    def display_variations(self, variations: list["BasePictograph"]) -> None:
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
        self.start_pos_cache = {
            "α": alpha_variations,
            "β": beta_variations,
            "Γ": gamma_variations,
        }
        all_variations: list["BasePictograph"] = (
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
        view_width = int(self.sequence_builder.height() // 5.5)
        return view_width

    def init_ui(self):
        variations = self.start_pos_picker.start_pos_manager.get_all_start_positions()
        self.display_variations(variations)

    def _resize_variation(self, variation: "BasePictograph") -> None:
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

    def on_variation_selected(self, variation: "BasePictograph") -> None:
        self.sequence_builder.start_pos_picker.start_pos_manager.on_start_pos_clicked(
            variation
        )

    def resize_advanced_start_pos_picker(self) -> None:
        self.ori_picker.resize_default_ori_picker()
