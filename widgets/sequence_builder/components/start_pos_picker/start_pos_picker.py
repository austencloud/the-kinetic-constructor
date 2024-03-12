from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QSize
from widgets.sequence_builder.components.start_pos_picker.start_pos_default_ori_picker import (
    StartPosDefaultOriPicker,
)

from widgets.sequence_builder.components.start_pos_picker.start_pos_pictograph_frame import (
    StartPosPickerPictographFrame,
)
from ....scroll_area.components.start_pos_picker_pictograph_factory import (
    StartPosPickerPictographFactory,
)
from .choose_your_start_pos_label import (
    ChooseYourStartPosLabel,
)

from .start_pos_manager import StartPosManager
from ....pictograph.pictograph import Pictograph
from .start_pos_variation_dialog import StartPosVariationDialog

if TYPE_CHECKING:
    from ...sequence_builder import SequenceBuilder


class StartPosPicker(QWidget):
    SPACING = 10

    def __init__(self, sequence_builder: "SequenceBuilder"):
        super().__init__(sequence_builder)
        self.sequence_builder = sequence_builder
        self.main_widget = sequence_builder.main_widget
        self.start_pos_cache: dict[str, Pictograph] = {}
        self.pictograph_factory = StartPosPickerPictographFactory(
            self, self.start_pos_cache
        )
        self.pictograph_frame = StartPosPickerPictographFrame(self)
        self.start_pos_manager = StartPosManager(self)
        self.choose_your_start_pos_label = ChooseYourStartPosLabel(self)
        self.button_layout = self._setup_variations_button_layout()
        self.setup_layout()

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
        self.layout.addLayout(self.button_layout, 1)
        self.layout.addStretch(1)

    def _setup_variations_button_layout(self):
        self.variations_button = QPushButton("Variations", self)
        self.variations_button.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        self.variations_button.setStyleSheet(
            """
            QPushButton {
                background-color: #446CB3;
                color: white;
                border-radius: 10px;
                padding: 10px;
                margin-top: 10px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #3D5C99;
            }
        """
        )
        self.variations_button.setFixedSize(QSize(200, 100))

        self.variations_button.clicked.connect(
            self.sequence_builder.show_advanced_start_pos_picker
        )

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.variations_button)
        button_layout.addStretch(1)
        return button_layout

    def get_variations(self, position: str) -> list[Pictograph]:
        variations = []
        for pictograph_dict in self.main_widget.letters[position]:
            pictograph = self.create_pictograph_from_dict(pictograph_dict)
            variations.append(pictograph)
        return variations

    def create_pictograph_from_dict(self, pictograph_dict: dict) -> Pictograph:
        pictograph = Pictograph(self.main_widget)
        pictograph.updater.update_pictograph(pictograph_dict)
        return pictograph

    def resize_start_pos_picker(self) -> None:
        self.pictograph_frame.resize_start_pos_picker_pictograph_frame()
        self.start_pos_manager.resize_start_position_pictographs()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.choose_your_start_pos_label.show()

    def show_variation_dialog(self, position: str) -> None:
        self.variation_dialog.resize_start_pos_variation_dialog()
        self.variation_dialog.load_variations(position)
        if self.variation_dialog.exec():
            selected_variation = self.variation_dialog.get_selected_variation()
            self.start_pos_manager.on_start_pos_clicked(selected_variation)
