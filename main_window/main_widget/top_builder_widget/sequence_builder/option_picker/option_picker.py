from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication, QCheckBox
from PyQt6.QtCore import pyqtSignal, Qt

from .option_getter import OptionGetter
from .choose_your_next_pictograph_label import ChooseYourNextPictographLabel
from .option_picker_scroll_area.option_picker_scroll_area import OptionPickerScrollArea
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.manual_builder import (
        ManualBuilder,
    )


class OptionPicker(QWidget):
    """Contains the "Choose Your Next Pictograph" label, filter checkboxes, and the OptionPickerScrollArea."""

    option_selected = pyqtSignal(str)

    def __init__(self, manual_builder: "ManualBuilder"):
        super().__init__(manual_builder)
        self.manual_builder = manual_builder
        self.main_widget = manual_builder.main_widget
        self.json_manager = self.main_widget.json_manager
        self.choose_your_next_pictograph_label = ChooseYourNextPictographLabel(self)
        self.option_getter = OptionGetter(self)
        self._setup_checkboxes()
        self.scroll_area = OptionPickerScrollArea(self)
        self.load_filters()

        # self.setStyleSheet("background-color: rgba(0, 0, 0, 200);")
        self.setup_layout()
        self.disabled = False
        self.hide()

    def setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.choose_your_next_pictograph_label.show()

        # Create header layout
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add the "Choose Your Next Pictograph" label
        header_label_layout = QHBoxLayout()
        header_label_layout.addStretch(1)
        header_label_layout.addWidget(self.choose_your_next_pictograph_label)
        header_label_layout.addStretch(1)
        header_layout.addLayout(header_label_layout)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        checkbox_layout.addWidget(self.continuous_checkbox)
        checkbox_layout.addWidget(self.prop_reversal_checkbox)
        checkbox_layout.addWidget(self.hand_reversal_checkbox)

        header_layout.addLayout(checkbox_layout)

        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.scroll_area, 14)

    def _setup_checkboxes(self):
        self.continuous_checkbox = QCheckBox("Continuous Motions")
        self.prop_reversal_checkbox = QCheckBox("Prop Reversals")
        self.hand_reversal_checkbox = QCheckBox("Hand Reversals")

        self.continuous_checkbox.setChecked(True)
        self.prop_reversal_checkbox.setChecked(True)
        self.hand_reversal_checkbox.setChecked(True)

        self.continuous_checkbox.stateChanged.connect(self.on_filter_changed)
        self.prop_reversal_checkbox.stateChanged.connect(self.on_filter_changed)
        self.hand_reversal_checkbox.stateChanged.connect(self.on_filter_changed)

    def on_filter_changed(self):
        """Called when any of the filter checkboxes change state."""
        self.save_filters()
        self.update_option_picker()

    def save_filters(self):
        filters = {
            "continuous_motions": self.continuous_checkbox.isChecked(),
            "prop_reversals": self.prop_reversal_checkbox.isChecked(),
            "hand_reversals": self.hand_reversal_checkbox.isChecked(),
        }
        self.main_widget.settings_manager.builder_settings.manual_builder.set_filters(
            filters
        )

    def load_filters(self):
        filters = (
            self.main_widget.settings_manager.builder_settings.manual_builder.get_filters()
        )
        self.continuous_checkbox.setChecked(filters.get("continuous_motions", True))
        self.prop_reversal_checkbox.setChecked(filters.get("prop_reversals", True))
        self.hand_reversal_checkbox.setChecked(filters.get("hand_reversals", True))

    def update_option_picker(self, sequence=None):
        if self.disabled:
            return
        if not sequence:
            sequence = self.json_manager.loader_saver.load_current_sequence_json()

        if len(sequence) > 1:
            # Get filter states
            filters = {
                'continuous_motions': self.continuous_checkbox.isChecked(),
                'prop_reversals': self.prop_reversal_checkbox.isChecked(),
                'hand_reversals': self.hand_reversal_checkbox.isChecked()
            }

            next_options: list = self.option_getter.get_next_options(sequence, filters)
            self.scroll_area._hide_all_pictographs()
            self.scroll_area.add_and_display_relevant_pictographs(next_options)
        self.choose_your_next_pictograph_label.set_stylesheet()


    def resize_option_picker(self) -> None:
        self.resize(self.manual_builder.width(), self.manual_builder.height())
        self.choose_your_next_pictograph_label.resize_choose_your_next_option_label()
        self.scroll_area.resize_option_picker_scroll_area()

    def set_disabled(self, disabled: bool) -> None:
        self.disabled = disabled
        self.scroll_area.set_disabled(disabled)
