from copy import deepcopy
import json
import os
from typing import TYPE_CHECKING, Literal
from PIL import Image
from path_helpers import get_images_and_data_path
from structural_variation_checker import StructuralVariationChecker
from thumbnail_generator import ThumbnailGenerator
from turn_pattern_variation_checker import TurnPatternVariationChecker

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class AddToDictionaryManager:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.json_handler = (
            sequence_widget.main_widget.json_manager.current_sequence_json_handler
        )
        self.thumbnail_generator = ThumbnailGenerator(self)
        dictionary_directory = get_images_and_data_path("dictionary")
        self.structural_checker = StructuralVariationChecker(dictionary_directory)

    def add_to_dictionary(self):
        current_sequence = self.json_handler.load_current_sequence_json()
        if self.is_sequence_invalid(current_sequence):
            self.display_message(
                "You must build a sequence to add it to your dictionary."
            )
            return
        self.process_sequence(current_sequence)

    def is_sequence_invalid(self, sequence):
        return len(sequence) <= 1

    def process_sequence(self, current_sequence):
        base_sequence = self.get_base_sequence(current_sequence)
        base_word = self.get_base_word(current_sequence)
        variation_exists, variation_number = (
            self.structural_checker.check_for_structural_variation(
                current_sequence, self.get_base_word
            )
        )
        directory = self.get_variation_directory(base_word, variation_number)
        turn_checker = TurnPatternVariationChecker(directory)

        if variation_exists:
            if turn_checker.check_for_turn_pattern_variation(current_sequence):
                self.display_message(
                    f"This exact variation of '{base_word}' is already saved in the dictionary."
                )
            else:
                self.save_variation(current_sequence, base_word, variation_number)
        else:
            self.process_new_variation(
                current_sequence, base_sequence, base_word, variation_number
            )

        self.refresh_ui()

    def process_new_variation(self, sequence, base_sequence, word, number):
        if self.sequence_has_turns(sequence):
            self.save_variation(sequence, word, number, "current")
            self.save_variation(base_sequence, word, number, "base")
            self.display_message(f"'{word}' with turns added to dictionary!")
        else:
            self.save_variation(sequence, word, number, "base")
            self.display_message(f"'{word}' added to dictionary!")

    def save_variation(self, sequence, word, number, type_label="base"):
        image_path = self.thumbnail_generator.generate_and_save_thumbnail(
            sequence, type_label, number
        )
        self.display_message(
            f"New {type_label} pattern of '{word}' saved as {os.path.basename(image_path)}."
        )

    def get_variation_directory(self, word, number):
        base_dir = get_images_and_data_path(f"dictionary/{word}")
        master_dir = os.path.join(base_dir, f"{word}_v{number}")
        return master_dir

    def display_message(self, message):
        self.sequence_widget.indicator_label.show_message(message)

    def refresh_ui(self):
        self.sequence_widget.main_widget.top_builder_widget.builder_toolbar.dictionary.reload_dictionary_tab()

    def get_base_word(self, sequence):
        base_sequence = []
        for entry in sequence:
            base_entry = entry.copy()
            base_sequence.append(base_entry)

        revalidated_sequence = self.revalidate_sequence(base_sequence)
        base_pattern = "".join(item.get("letter", "") for item in revalidated_sequence)
        base_pattern = base_pattern[1:]
        return base_pattern

    def get_base_sequence(self, sequence):
        # Create a deep copy of the sequence to avoid modifying the original
        base_sequence = deepcopy(sequence)
        for entry in base_sequence:
            entry["blue_attributes"]["turns"] = 0
            entry["red_attributes"]["turns"] = 0

        self.revalidate_sequence(base_sequence)
        return base_sequence


    def revalidate_sequence(self, sequence):
        if not hasattr(self, "validation_engine"):
            self.validation_engine = self.json_handler.validation_engine
        self.validation_engine.sequence = sequence
        self.validation_engine.run()
        return self.validation_engine.sequence

    def sequence_has_turns(self, current_sequence):
        for beat in current_sequence[1:]:
            if (
                beat.get("blue_attributes", {}).get("turns", 0) != 0
                or beat.get("red_attributes", {}).get("turns", 0) != 0
            ):
                return True
