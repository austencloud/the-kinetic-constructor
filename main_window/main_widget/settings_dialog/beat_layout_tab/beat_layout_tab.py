from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog

from ...sequence_widget.beat_frame.layout_warning_dialog import LayoutWarningDialog
from ...sequence_widget.beat_frame.layout_options_beat_frame import (
    SequenceLayoutOptionsBeatFrame,
)
from .beat_layout_options_panel import BeatLayoutOptionsPanel

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class BeatLayoutTab(QWidget):
    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__(settings_dialog)
        self.sequence_widget = settings_dialog.main_widget.sequence_widget
        self.settings_manager = (
            self.sequence_widget.main_widget.main_window.settings_manager
        )
        initial_state = self.sequence_widget.beat_frame.get.current_beat_frame_state()

        self.beat_frame = SequenceLayoutOptionsBeatFrame(self)
        self.panel = BeatLayoutOptionsPanel(self)

        self._setup_apply_button()
        self._setup_layout()

        if initial_state:
            self.panel.initialize_from_state(initial_state)
        else:
            self.panel.load_settings()

    def _setup_apply_button(self):
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.panel, 3)
        layout.addWidget(self.beat_frame, 9)
        layout.addWidget(self.apply_button)

    def apply_settings(self):
        grow_sequence = self.panel.grow_sequence_checkbox.isChecked()
        num_filled_beats = (
            self.sequence_widget.beat_frame.get.next_available_beat() - 1 or 0
        )
        if grow_sequence:
            self.settings_manager.global_settings.set_grow_sequence(True)
            self.sequence_widget.beat_frame.layout_manager.configure_beat_frame(
                num_filled_beats + 1
            )
        else:
            self.settings_manager.global_settings.set_grow_sequence(False)
            num_beats = int(self.panel.beats_combo_box.currentText())
            selected_layout = self.panel.layout_combo_box.currentText()
            cols, rows = map(int, selected_layout.split(" x "))
            if num_beats < num_filled_beats:
                if self.open_warning_dialog():
                    self.sequence_widget.layout_manager.apply_layout_options(
                        rows, cols, num_beats
                    )
                    for i in range(num_beats, num_filled_beats):
                        self.sequence_widget.beat_frame.beat_views[i].setScene(
                            self.sequence_widget.beat_frame.beat_views[i].blank_beat
                        )
                    selected_beat = (
                        self.sequence_widget.beat_frame.selection_overlay.selected_beat
                    )
                    if selected_beat:
                        selected_beat_index = selected_beat.number - 1
                        if (
                            selected_beat_index is not None
                            and selected_beat_index >= num_beats
                        ):
                            self.sequence_widget.beat_frame.selection_overlay.select_beat(
                                self.sequence_widget.beat_frame.beat_views[
                                    num_beats - 1
                                ]
                            )
                else:
                    return
            else:
                self.sequence_widget.layout_manager.apply_layout_options(
                    cols, rows, num_beats
                )

    def open_warning_dialog(self):
        dialog = LayoutWarningDialog(self)
        result = dialog.exec()
        return result == QDialog.DialogCode.Accepted
