from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication
from PyQt6.QtCore import pyqtSignal, Qt

from .toggle_with_label import ToggleWithLabel  # Import the new class

from .option_getter import OptionGetter
from .choose_your_next_pictograph_label import ChooseYourNextPictographLabel
from .option_picker_scroll_area.option_picker_scroll_area import OptionPickerScrollArea
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.manual_builder import (
        ManualBuilder,
    )


class OptionPicker(QWidget):
    """Contains the 'Choose Your Next Pictograph' label, filter toggles, and the OptionPickerScrollArea."""

    option_selected = pyqtSignal(str)

    def __init__(self, manual_builder: "ManualBuilder"):
        super().__init__(manual_builder)
        self.manual_builder = manual_builder
        self.main_widget = manual_builder.main_widget
        self.json_manager = self.main_widget.json_manager
        self.disabled = False
        self.choose_your_next_pictograph_label = ChooseYourNextPictographLabel(self)
        self.option_getter = OptionGetter(self)
        self._setup_toggles()
        self.scroll_area = OptionPickerScrollArea(self)

        self.setup_layout()
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

        # Add toggles to the layout
        self.toggle_layout = QHBoxLayout()
        self.toggle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.toggle_layout.addWidget(self.continuous_toggle)
        self.toggle_layout.addWidget(self.one_reversal_toggle)
        self.toggle_layout.addWidget(self.two_reversals_toggle)

        header_layout.addLayout(self.toggle_layout)

        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.scroll_area, 14)

    def _setup_toggles(self):
        self.continuous_toggle = ToggleWithLabel("Continuous", self)
        self.one_reversal_toggle = ToggleWithLabel("One Reversal", self)
        self.two_reversals_toggle = ToggleWithLabel("Two Reversals", self)
        self.toggles: dict[str, ToggleWithLabel] = {
            "continuous": self.continuous_toggle,
            "one_reversal": self.one_reversal_toggle,
            "two_reversals": self.two_reversals_toggle,
        }

        self._load_filters()
        for toggle_widget in self.toggles.values():
            toggle_widget.toggle.stateChanged.connect(self.on_filter_changed)

    def on_filter_changed(self):
        """Called when any of the filter toggles change state."""
        self.save_filters()
        self.update_option_picker()

    def save_filters(self):
        filters = {
            "continuous": self.continuous_toggle.toggle.isChecked(),
            "one_reversal": self.one_reversal_toggle.toggle.isChecked(),
            "two_reversals": self.two_reversals_toggle.toggle.isChecked(),
        }
        self.main_widget.settings_manager.builder_settings.manual_builder.set_filters(
            filters
        )

    def _load_filters(self):
        filters = (
            self.main_widget.settings_manager.builder_settings.manual_builder.get_filters()
        )
        self.continuous_toggle.toggle.setChecked(filters.get("continuous", True))
        self.one_reversal_toggle.toggle.setChecked(filters.get("one_reversal", True))
        self.two_reversals_toggle.toggle.setChecked(filters.get("two_reversals", True))

    def update_option_picker(self, sequence=None):
        if self.disabled:
            return
        if not sequence:
            sequence = self.json_manager.loader_saver.load_current_sequence_json()

        if len(sequence) > 2:
            # Get filter states
            filters = {
                "continuous": self.continuous_toggle.toggle.isChecked(),
                "one_reversal": self.one_reversal_toggle.toggle.isChecked(),
                "two_reversals": self.two_reversals_toggle.toggle.isChecked(),
            }

            next_options: list = self.option_getter.get_next_options(sequence, filters)
            self.scroll_area.clear_pictographs()  # Clear existing pictographs
            self.scroll_area.add_and_display_relevant_pictographs(next_options)
        elif len(sequence) == 2:
            self.scroll_area.clear_pictographs()
            next_options = self.option_getter._load_all_next_options(sequence)
            self.scroll_area.add_and_display_relevant_pictographs(next_options)
        self.choose_your_next_pictograph_label.set_stylesheet()

    def resize_option_picker(self) -> None:
        self.resize(self.manual_builder.width(), self.manual_builder.height())
        self.choose_your_next_pictograph_label.resize_choose_your_next_option_label()
        self.scroll_area.resize_option_picker_scroll_area()
        for toggle_widget in self.toggles.values():
            font = toggle_widget.label.font()
            toggle_font_size = self.manual_builder.width() // 65
            font.setPointSize(toggle_font_size)
            font.setFamily("Georgia")
            toggle_widget.label.setFont(font)
        spacing = self.manual_builder.width() // 20
        self.toggle_layout.setSpacing(spacing)

    def set_disabled(self, disabled: bool) -> None:
        self.disabled = disabled
        self.scroll_area.set_disabled(disabled)
