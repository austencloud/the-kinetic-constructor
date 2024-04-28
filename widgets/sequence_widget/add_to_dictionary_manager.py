import json
import os
from typing import TYPE_CHECKING, Literal
from PIL import Image
from path_helpers import get_images_and_data_path
from thumbnail_generator import ThumbnailGenerator

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class AddToDictionaryManager:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.json_handler = (
            sequence_widget.main_widget.json_manager.current_sequence_json_handler
        )
        self.beat_frame = sequence_widget.beat_frame
        self.indicator_label = sequence_widget.indicator_label
        self.main_widget = sequence_widget.main_widget
        self.thumbnail_generator = ThumbnailGenerator(self)

    def add_to_dictionary(self):
        current_sequence = self.json_handler.load_current_sequence_json()

        if len(current_sequence) <= 1:
            self.indicator_label.show_message(
                "You must build a sequence to add it to your dictionary."
            )
            return

        has_non_zero_turns = any(
            beat.get("blue_attributes", {}).get("turns", 0) != 0
            or beat.get("red_attributes", {}).get("turns", 0) != 0
            for beat in current_sequence
        )

        base_sequence = self.get_base_sequence(current_sequence)
        base_word = self.get_base_word(current_sequence)
        variation_exists, master_dir, structural_variation_number = (
            self.check_for_structural_variation(current_sequence)
        )
        structural_variation_directory = self.get_structural_variation_directory(
            base_word, structural_variation_number
        )
        if variation_exists:
            if self.structural_variation_already_saved(
                master_dir,
                current_sequence,
                has_non_zero_turns,
                structural_variation_directory,
            ):
                self.indicator_label.show_message(
                    f"The exact variation of '{base_word}' is already saved in the dictionary."
                )
            else:
                # If it's a new turn pattern, save it
                image_path = self.thumbnail_generator.generate_and_save_thumbnail(
                    current_sequence,
                    "current" if has_non_zero_turns else "base",
                    structural_variation_number,
                )
                self.indicator_label.show_message(
                    f"New turn pattern of '{base_word}' saved as {os.path.basename(image_path)}."
                )
        else:
            # No structural variation exists, save both current and base (if there are turns)
            if has_non_zero_turns:
                self.thumbnail_generator.generate_and_save_thumbnail(
                    current_sequence, "current", structural_variation_number
                )
                self.thumbnail_generator.generate_and_save_thumbnail(
                    base_sequence, "base", structural_variation_number
                )
                self.indicator_label.show_message(
                    f"'{base_word}' with turns added to dictionary!"
                )
            else:
                self.thumbnail_generator.generate_and_save_thumbnail(
                    current_sequence, "base", structural_variation_number
                )
                self.indicator_label.show_message(f"'{base_word}' added to dictionary!")

        self.main_widget.top_builder_widget.builder_toolbar.dictionary.reload_dictionary_tab()

    def get_structural_variation_directory(
        self, base_word, structural_variation_number
    ):
        base_dir = get_images_and_data_path(f"thumbnails/{base_word}")
        master_dir = os.path.join(
            base_dir, f"{base_word}_v{structural_variation_number}"
        )
        return master_dir

    def check_for_structural_variation(
        self, new_sequence
    ) -> tuple[Literal[True], str, str] | tuple[Literal[False], None, Literal["1"]]:
        thumbnail_dir = get_images_and_data_path("thumbnails")
        for item in os.scandir(thumbnail_dir):
            if item.is_dir():
                base_word_folder = item.path
                for structural_variation_folder in os.listdir(base_word_folder):
                    for sequence in os.listdir(
                        os.path.join(base_word_folder, structural_variation_folder)
                    ):
                        image_path = os.path.join(
                            base_word_folder, structural_variation_folder, sequence
                        )
                        if os.path.isfile(
                            image_path
                        ):  # Only proceed if the path is a file
                            with Image.open(image_path) as img:
                                metadata = img.info.get("metadata")
                                if metadata:
                                    saved_sequence = json.loads(metadata)
                                    if self.are_structural_variations_identical(
                                        saved_sequence, new_sequence
                                    ):
                                        version_number = (
                                            structural_variation_folder.split("_v")[-1]
                                        )
                                        return True, base_word_folder, version_number

        if os.path.exists(thumbnail_dir):
            base_word = self.get_base_word(new_sequence)
            version_number = 1
            while os.path.exists(
                os.path.join(thumbnail_dir, f"{base_word}", f"{base_word}_v{version_number}")
            ):
                version_number += 1
            return False, None, str(version_number)

        return False, None, "1"

    def structural_variation_already_saved(
        self,
        master_dir,
        current_sequence,
        has_non_zero_turns,
        structural_variation_directory,
    ):
        for image_name in os.listdir(structural_variation_directory):
            image_path = os.path.join(structural_variation_directory, image_name)
            with Image.open(image_path) as img:
                metadata = img.info.get("metadata")
                if metadata:
                    saved_sequence = json.loads(metadata)
                    if self.are_turn_patterns_identical(
                        saved_sequence, current_sequence
                    ):
                        return True
        return False

    def are_turn_patterns_identical(self, seq1, seq2):
        for beat1, beat2 in zip(seq1, seq2):
            for attribute in ["blue_attributes", "red_attributes"]:
                if attribute != "turns":
                    continue
                if attribute in beat1 and attribute in beat2:
                    if beat1[attribute] != beat2[attribute]:
                        return False
                else:
                    return False
        return True

    def are_structural_variations_identical(self, seq1, seq2) -> TYPE_CHECKING:
        # Helper function to check if two beats are structurally the same
        def beats_are_same(b1, b2) -> bool:
            ignored_keys = ["turns", "end_ori"]
            for key in b1.keys():
                if key not in ignored_keys and b1[key] != b2[key]:
                    return False
            return True

        if len(seq1) != len(seq2):
            return False

        for beat1, beat2 in zip(seq1, seq2):
            for color in ["blue_attributes", "red_attributes"]:
                if color in beat1 and color in beat2:
                    if not beats_are_same(beat1[color], beat2[color]):
                        return False
                else:
                    # One of the sequences does not have either blue or red attributes
                    return False
        return True

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
        base_sequence = []
        for entry in sequence:
            base_entry = entry.copy()
            base_entry["blue_attributes"]["turns"] = 0
            base_entry["red_attributes"]["turns"] = 0
            base_sequence.append(base_entry)

        self.revalidate_sequence(base_sequence)
        return base_sequence

    def revalidate_sequence(self, sequence):
        if not hasattr(self, "validation_engine"):
            self.validation_engine = (
                self.main_widget.json_manager.current_sequence_json_handler.validation_engine
            )
        self.validation_engine.sequence = sequence
        self.validation_engine.run()
        return self.validation_engine.sequence
