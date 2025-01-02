from typing import TYPE_CHECKING

from base_widgets.base_go_back_button import (
    BaseGoBackButton,
)


if TYPE_CHECKING:
    from .sequence_picker import SequencePicker


class SequencePickerGoBackButton(BaseGoBackButton):
    def __init__(self, sequence_picker: "SequencePicker"):
        super().__init__(sequence_picker.main_widget)
        self.sequence_picker = sequence_picker
        self.browse_tab = self.sequence_picker.browse_tab
        self.main_widget = self.sequence_picker.main_widget
        self.clicked.connect(lambda: self.switch_to_initial_filter_selection())

    def switch_to_initial_filter_selection(self):
        """Switch to the initial selection page in the stacked layout."""
        sequence_viewer = self.browse_tab.sequence_viewer
        sequence_viewer.word_label.setText("")
        self.main_widget.fade_manager.stack_fader.fade_stack(
            self.main_widget.left_stack, self.main_widget.left_filter_selector_index
        )

        self.browse_tab.sequence_viewer.clear()
        self.browse_tab.settings.set_current_section("filter_choice")
        self.browse_tab.settings.set_current_filter(None)
        self.sequence_picker.filter_stack.show_section("filter_choice")
