from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from typing import TYPE_CHECKING
from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from .start_pos_picker import StartPosPicker


class StartPosPickerPictographFrame(QWidget):
    def __init__(self, start_pos_picker: "StartPosPicker") -> None:
        super().__init__(start_pos_picker)
        self.start_pos_picker = start_pos_picker
        self.clickable_option_handler = (
            self.start_pos_picker.sequence_builder.option_click_handler
        )
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.pictographs_layout = QHBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.pictographs_layout)
        self.layout.addLayout(self.buttons_layout)
        self.variation_buttons: dict[str, QPushButton] = {}
        self.start_positions: dict[str, Pictograph] = {}
        
        
    def resize_start_pos_picker_pictograph_frame(self) -> None:
        self.setMinimumWidth(self.start_pos_picker.width())
        self.start_pos_picker.choose_your_start_pos_label.set_stylesheet()
        for button in self.variation_buttons.values():
            button.setMaximumWidth(
                self.start_positions[list(self.start_positions.keys())[0]].view.width()
            )

    def _add_start_pos_to_layout(self, start_pos: Pictograph) -> None:
        start_pos.view.mousePressEvent = (
            self.clickable_option_handler.get_click_handler(start_pos)
        )
        self.pictographs_layout.addWidget(start_pos.view)
        self.start_pos_picker.start_pos_cache[start_pos.letter] = start_pos
        key = f"{start_pos.letter}_{start_pos.start_pos}_{start_pos.end_pos}"
        self.start_pos_picker.main_widget.all_pictographs[start_pos.letter][
            key
        ] = start_pos
        self.start_positions[start_pos.letter] = start_pos
        variation_button = self._setup_variation_button(start_pos)
        self.buttons_layout.addWidget(variation_button)

    def _setup_variation_button(self, start_pos: Pictograph) -> QPushButton:
        variation_button = QPushButton(f"Select {start_pos.letter} Variation")
        variation_button.clicked.connect(
            lambda _, pos=start_pos.letter: self.start_pos_picker.show_variation_dialog(pos)
        )
        self.variation_buttons[start_pos.letter] = variation_button
        return variation_button
