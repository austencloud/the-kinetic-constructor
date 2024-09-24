from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from .start_pos_picker_variations_button import StartPosVariationsButton
from .start_pos_pictograph_frame import StartPosPickerPictographFrame
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from .start_pos_manager import StartPosManager
from .choose_your_start_pos_label import ChooseYourStartPosLabel
if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.manual_builder import (
        ManualBuilder,
    )


class StartPosPicker(QWidget):
    SPACING = 10

    def __init__(self, manual_builder: "ManualBuilder"):
        super().__init__(manual_builder)
        self.manual_builder = manual_builder
        self.main_widget = manual_builder.main_widget
        self.start_pos_cache: dict[str, BasePictograph] = {}

        self.pictograph_frame = StartPosPickerPictographFrame(self)
        self.start_pos_manager = StartPosManager(self)
        self.choose_your_start_pos_label = ChooseYourStartPosLabel(self)
        self.button_layout = self._setup_variations_button_layout()
        self.setup_layout()
        self.setObjectName("StartPosPicker")
        self.setStyleSheet("background-color: white;")
        self.initialized = False

    def setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        start_label_layout = QHBoxLayout()
        pictograph_layout = QHBoxLayout()

        start_label_layout.addWidget(self.choose_your_start_pos_label)
        pictograph_layout.addWidget(self.pictograph_frame)

        self.layout.addStretch(1)
        self.layout.addLayout(start_label_layout)
        self.layout.addStretch(1)
        self.layout.addLayout(pictograph_layout)
        self.layout.addStretch(1)
        self.layout.addLayout(self.button_layout)
        self.layout.addStretch(1)

    def _setup_variations_button_layout(self) -> QHBoxLayout:
        self.variations_button = StartPosVariationsButton(self)

        self.variations_button.clicked.connect(
            self.manual_builder.transition_to_advanced_start_pos_picker
        )

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.variations_button)
        button_layout.addStretch(1)
        return button_layout

    def get_variations(self, position: str) -> list[BasePictograph]:
        variations = []
        for pictograph_dict in self.main_widget.pictograph_dicts[position]:
            pictograph = self.create_pictograph_from_dict(pictograph_dict)
            variations.append(pictograph)
        return variations

    def create_pictograph_from_dict(self, pictograph_dict: dict) -> BasePictograph:
        pictograph = BasePictograph(self.main_widget)
        pictograph.updater.update_pictograph(pictograph_dict)
        return pictograph

    def resize_start_pos_picker(self) -> None:
        self.pictograph_frame.resize_start_pos_picker_pictograph_frame()
        self.start_pos_manager.resize_start_position_pictographs()
        self.variations_button.resize_variations_button()

