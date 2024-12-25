from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .main_widget import MainWidget


class MainWidgetState:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def load_state(self):
        current_sequence = (
            self.main_widget.json_manager.sequence_loader_saver.load_current_sequence_json()
        )
        if len(current_sequence) > 1:
            self.main_widget.build_tab.sequence_constructor.transition_to_sequence_building()
            self.main_widget.build_tab.sequence_widget.beat_frame.populator.populate_beat_frame_from_json(
                current_sequence
            )
            self.main_widget.build_tab.sequence_constructor.option_picker.update_option_picker()
