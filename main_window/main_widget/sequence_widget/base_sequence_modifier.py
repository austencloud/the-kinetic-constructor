from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class BaseSequenceModifier:
    success_message: str
    error_message: str

    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.json_loader = self.sequence_widget.main_widget.json_manager.loader_saver

    def _update_ui(self):
        """Update all UI components after a modification."""
        self.sequence_widget.main_widget.construct_tab.option_picker.updater.refresh_options()
        self.sequence_widget.graph_editor.update_graph_editor()
        self.sequence_widget.indicator_label.show_message(self.success_message)

    def _check_length(self):
        """Check if the sequence is long enough to modify."""
        current_sequence = self.json_loader.load_current_sequence_json()

        if len(current_sequence) < 2:
            self.sequence_widget.indicator_label.show_message(self.error_message)
            QApplication.restoreOverrideCursor()
            return False
        return True
