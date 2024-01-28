import os
from typing import TYPE_CHECKING
from Enums import LetterType
from constants import Type1
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.MotionAttributes import Colors
from utilities.TypeChecking.letter_lists import Type1_non_hybrid_letters
from widgets.pictograph.components.placement_managers.arrow_placement_manager.handlers.special_arrow_positioner.handlers.special_placement_json_handler import SpecialPlacementJsonDataHandler

if TYPE_CHECKING:
    from widgets.pictograph.components.placement_managers.arrow_placement_manager.handlers.special_arrow_positioner.handlers.special_placement_data_updater import MirroredTupleHandler, SpecialPlacementDataUpdater
class SpecialPlacementEntryRemover:
    """Handles removal of special placement entries."""

    def __init__(
        self,
        data_updater: "SpecialPlacementDataUpdater",
    ) -> None:
        self.positioner = data_updater.positioner
        self.data_updater = data_updater

    def remove_special_placement_entry(self, letter: str, arrow: Arrow) -> None:
        if (
            not LetterType.get_letter_type(arrow.pictograph.letter) == Type1
            or arrow.pictograph.letter not in Type1_non_hybrid_letters
        ):
            return

        orientation_key = self.data_updater._get_orientation_key(arrow.motion.start_ori)
        file_path = os.path.join(
            self.positioner.placement_manager.pictograph.main_widget.parent_directory,
            f"{orientation_key}/{letter}_placements.json",
        )

        if os.path.exists(file_path):
            data = SpecialPlacementJsonDataHandler.load_json_data(file_path)
            if letter in data:
                letter_data = data[letter]
                turns_tuple = (
                    self.positioner.turns_tuple_generator.generate_turns_tuple(letter)
                )

                self._remove_turn_data_entry(letter_data, turns_tuple, arrow.color)
                mirrored_turns_tuple = MirroredTupleHandler.mirror_turns_tuple(
                    turns_tuple
                )
                if mirrored_turns_tuple:
                    mirrored_color = "blue" if arrow.color == "red" else "red"
                    self._remove_turn_data_entry(
                        letter_data, mirrored_turns_tuple, mirrored_color
                    )

                SpecialPlacementJsonDataHandler.write_json_data(data, file_path)
            arrow.pictograph.main_widget.refresh_placements()

    def _remove_turn_data_entry(
        self, letter_data: dict, turns_tuple: str, color: Colors
    ) -> None:
        turn_data = letter_data.get(turns_tuple, {})
        if color in turn_data:
            del turn_data[color]
            if not turn_data:
                del letter_data[turns_tuple]
