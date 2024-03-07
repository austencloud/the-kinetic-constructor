from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton
from ....pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_builder.components.start_position_picker.start_pos_picker import StartPosPicker


class StartPosVariationDialog(QDialog):
    def __init__(self, start_pos_picker: "StartPosPicker"):
        super().__init__(start_pos_picker)
        self.start_pos_picker = start_pos_picker
        # self.variation_picker = StartPosVariationPicker(self)
        # self.ori_changer = StartPosOriChanger(self)
        self.selected_variation: Pictograph = None

        # self.setup_layout()

    def setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(self.variation_picker)
        layout.addWidget(self.ori_changer)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def load_variations(self, position: str) -> None:
        variations = self.start_pos_picker.start_pos_manager.get_variations(position)
        self.variation_picker.display_variations(variations)

    def get_selected_variation(self) -> Pictograph:
        return self.variation_picker.get_selected_variation()
