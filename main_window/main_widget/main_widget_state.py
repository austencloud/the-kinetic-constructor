from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_widget import MainWidget


class MainWidgetState:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def save_state(self):
        self.main_widget.json_manager.loader_saver.save_current_sequence(
            self.main_widget.json_manager.loader_saver.load_current_sequence_json()
        )
        self.main_widget.settings_manager.save_settings()

    def load_state(self):
        self.main_widget.settings_manager.load_settings()
        current_sequence = (
            self.main_widget.json_manager.loader_saver.load_current_sequence_json()
        )
        if len(current_sequence) > 1:
            self.main_widget.manual_builder.transition_to_sequence_building()
            self.main_widget.sequence_widget.beat_frame.populator.populate_beat_frame_from_json(
                current_sequence
            )
            self.main_widget.manual_builder.option_picker.update_option_picker()
