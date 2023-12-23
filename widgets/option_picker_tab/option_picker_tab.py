from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QCheckBox
from .option_picker_scroll import OptionPickerScroll
if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
from widgets.option_picker_tab.option_picker_filter_frame import OptionPickerFilterFrame
class OptionPickerTab(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.main_layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.option_picker_filter_frame = OptionPickerFilterFrame(self)
        self.filter_layout = QHBoxLayout(self.filter_frame)
        self.option_picker = OptionPickerScroll(self.main_widget, self)

        # Create checkboxes for each turn value
        self.turn_checkboxes = {}
        for turn_value in ["fl", 0, 0.5, 1, 1.5, 2, 2.5, 3]:
            checkbox = QCheckBox(str(turn_value), self.filter_frame)
            checkbox.stateChanged.connect(self.apply_filters)
            self.filter_layout.addWidget(checkbox)
            self.turn_checkboxes[turn_value] = checkbox

        self.main_layout.addWidget(self.filter_frame)
        self.main_layout.addWidget(self.option_picker)

    def apply_filters(self):
        selected_turns = [
            turn
            for turn, checkbox in self.turn_checkboxes.items()
            if checkbox.isChecked()
        ]
        self.option_picker.apply_turn_filters(selected_turns)
