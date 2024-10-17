from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
    QComboBox,
    QLabel,
)
from PyQt6.QtCore import pyqtSignal, Qt


from .toggle_with_label import ToggleWithLabel  # Import the new class

from .option_getter import OptionGetter
from .choose_your_next_pictograph_label import ChooseYourNextPictographLabel
from .option_picker_scroll_area.option_picker_scroll_area import OptionPickerScrollArea
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.sequence_builder.manual_builder import (
        ManualBuilderWidget,
    )


class OptionPicker(QWidget):
    """Contains the 'Choose Your Next Pictograph' label, filter combo box, and the OptionPickerScrollArea."""

    option_selected = pyqtSignal(str)

    def __init__(self, manual_builder: "ManualBuilderWidget"):
        super().__init__(manual_builder)
        self.manual_builder = manual_builder
        self.main_widget = manual_builder.main_widget
        self.json_manager = self.main_widget.json_manager
        self.disabled = False
        self.choose_your_next_pictograph_label = ChooseYourNextPictographLabel(self)
        self.option_getter = OptionGetter(self)
        self._setup_combo_box()
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

        # Add combo box to the layout
        self.combo_box_layout = QHBoxLayout()
        self.combo_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.combo_box_label: QLabel = QLabel("Prop-reversals:")
        self.combo_box_layout.addWidget(self.combo_box_label)
        self.combo_box_layout.addWidget(self.filter_combo_box)
        header_layout.addLayout(self.combo_box_layout)

        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.scroll_area, 14)

    def _setup_combo_box(self):
        self.filter_combo_box = QComboBox(self)
        self.filter_combo_box.addItem("All", userData=None)
        self.filter_combo_box.addItem("Continuous", userData="continuous")
        self.filter_combo_box.addItem("One Reversal", userData="one_reversal")
        self.filter_combo_box.addItem("Two Reversals", userData="two_reversals")
        self.filter_combo_box.setCursor(Qt.CursorShape.PointingHandCursor)
        self._load_filter()
        self.filter_combo_box.currentIndexChanged.connect(self.on_filter_changed)

    def on_filter_changed(self):
        """Called when the filter combo box selection changes."""
        self.save_filter()
        self.update_option_picker()

    def save_filter(self):
        selected_filter = self.filter_combo_box.currentData()
        self.main_widget.settings_manager.builder_settings.manual_builder.set_filters(
            selected_filter
        )

    def _load_filter(self):
        selected_filter = (
            self.main_widget.settings_manager.builder_settings.manual_builder.get_filters()
        )
        index = self.filter_combo_box.findData(selected_filter)
        if index != -1:
            self.filter_combo_box.setCurrentIndex(index)
        else:
            self.filter_combo_box.setCurrentIndex(0)  # Default to "All"

    def update_option_picker(self, sequence=None):
        if self.disabled:
            return
        if not sequence:
            sequence = self.json_manager.loader_saver.load_current_sequence_json()

        if len(sequence) > 2:
            # Get selected filter
            selected_filter = self.filter_combo_box.currentData()

            next_options: list = self.option_getter.get_next_options(
                sequence, selected_filter
            )
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
        self._resize_combo_box()

    def _resize_combo_box(self):
        font = self.filter_combo_box.font()
        font_size = int(self.manual_builder.width() * 0.015)
        font.setPointSize(font_size)
        font.setFamily("Georgia")
        self.filter_combo_box.setFont(font)
        self.combo_box_label.setFont(font)

    def set_disabled(self, disabled: bool) -> None:
        self.disabled = disabled
        self.scroll_area.set_disabled(disabled)
