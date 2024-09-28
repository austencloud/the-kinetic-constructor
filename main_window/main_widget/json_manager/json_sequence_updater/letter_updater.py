from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from main_window.main_widget.json_manager.json_manager import JsonManager


class LetterUpdater:
    def __init__(self, json_manager: "JsonManager"):
        self.json_manager = json_manager

    def update_letter_in_json_at_index(self, index: int, letter: str) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        sequence[index]["letter"] = letter
        self.json_manager.loader_saver.save_current_sequence(sequence)
