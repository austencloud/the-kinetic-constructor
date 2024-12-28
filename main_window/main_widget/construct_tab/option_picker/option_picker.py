from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt

from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.construct_tab.option_picker.option_picker_pictograph_view import (
    OptionPickerPictographView,
)
from .option_picker_reversal_selector import OptionPickerReversalSelector
from .option_getter import OptionGetter
from .choose_your_next_pictograph_label import ChooseYourNextPictographLabel
from .option_picker_scroll_area.option_picker_scroll_area import OptionPickerScrollArea
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..construct_tab import ConstructTab


class OptionPicker(QWidget):
    """Contains the 'Choose Your Next Pictograph' label, filter combo box, and the OptionPickerScrollArea."""

    COLUMN_COUNT = 8
    option_selected = pyqtSignal(str)

    def __init__(self, construct_tab: "ConstructTab"):
        super().__init__(construct_tab)
        self.construct_tab = construct_tab
        self.main_widget = construct_tab.main_widget
        self.json_manager = self.main_widget.json_manager
        self.disabled = False
        self.choose_your_next_pictograph_label = ChooseYourNextPictographLabel(self)
        self.option_getter = OptionGetter(self)
        self.scroll_area = OptionPickerScrollArea(self)
        self.reversal_selector = OptionPickerReversalSelector(self)
        self.option_pool: list[BasePictograph] = []
        # Decide on a max number based on the largest number of options typically displayed.
        MAX_PICTOGRAPHS = 36
        for _ in range(MAX_PICTOGRAPHS):
            option = BasePictograph(self.main_widget)
            option.view = OptionPickerPictographView(option, self)
            option.view.hide()  # Keep them hidden until needed
            self.option_pool.append(option)

        self._load_filter()
        self.setup_layout()
        self.hide()

    def setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.choose_your_next_pictograph_label.show()

        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_label_layout = QHBoxLayout()
        header_label_layout.addWidget(self.choose_your_next_pictograph_label)
        header_layout.addLayout(header_label_layout)
        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.reversal_selector)
        self.layout.addWidget(self.scroll_area, 14)

    def on_filter_changed(self):
        """Called when the filter combo box selection changes."""
        self.save_filter()
        self.update_option_picker()

    def save_filter(self):
        selected_filter = self.reversal_selector.reversal_combobox.currentData()
        self.main_widget.settings_manager.builder_settings.manual_builder.set_filters(
            selected_filter
        )

    def _load_filter(self):
        selected_filter = (
            self.main_widget.settings_manager.builder_settings.manual_builder.get_filters()
        )
        index = self.reversal_selector.reversal_combobox.findData(selected_filter)
        if index != -1:
            self.reversal_selector.reversal_combobox.setCurrentIndex(index)
        else:
            self.reversal_selector.reversal_combobox.setCurrentIndex(0)

    def update_option_picker(self, sequence=None):
        if self.disabled:
            return
        if not sequence:
            sequence = self.json_manager.loader_saver.load_current_sequence_json()

        if len(sequence) > 2:
            selected_filter = self.reversal_selector.reversal_combobox.currentData()

            next_options: list = self.option_getter.get_next_options(
                sequence, selected_filter
            )
            self.scroll_area.clear_pictographs()
            self.scroll_area.add_and_display_relevant_pictographs(next_options)

        elif len(sequence) == 2:
            self.scroll_area.clear_pictographs()
            next_options = self.option_getter._load_all_next_options(sequence)
            self.scroll_area.add_and_display_relevant_pictographs(next_options)

    def set_disabled(self, disabled: bool) -> None:
        self.disabled = disabled
        self.scroll_area.set_disabled(disabled)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        spacing = 10
        for option in self.option_pool:
            view_width = int((self.width() // 8) - spacing)

            option.view.setFixedSize(view_width, view_width)
            option.view.view_scale = view_width / option.width()
            option.view.resetTransform()
            option.view.scale(option.view.view_scale, option.view.view_scale)
