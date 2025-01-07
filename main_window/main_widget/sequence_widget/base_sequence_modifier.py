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

    def update_ui(self):
        """Update all UI components after a modification."""
        self.sequence_widget.main_widget.construct_tab.option_picker.update_option_picker()
        self.sequence_widget.graph_editor.update_graph_editor()
        self.sequence_widget.indicator_label.show_message(self.success_message)

    def check_length(self, current_sequence):
        """Check if the sequence is long enough to modify."""
        if len(current_sequence) < 2:
            self.sequence_widget.indicator_label.show_message(self.error_message)
            QApplication.restoreOverrideCursor()
            return False

