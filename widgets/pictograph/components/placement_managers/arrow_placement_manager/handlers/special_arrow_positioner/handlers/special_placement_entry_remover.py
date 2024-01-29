import os
from typing import TYPE_CHECKING, Union
from Enums import LetterType
from constants import Type1, Type4
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.MotionAttributes import Colors
from utilities.TypeChecking.letter_lists import non_hybrid_letters


if TYPE_CHECKING:
    from widgets.pictograph.components.placement_managers.arrow_placement_manager.handlers.special_arrow_positioner.handlers.special_placement_data_updater import (
        MirroredTupleHandler,
        SpecialPlacementDataUpdater,
    )


class SpecialPlacementEntryRemover:
    """Handles removal of special placement entries."""

    def __init__(
        self,
        data_updater: "SpecialPlacementDataUpdater",
    ) -> None:
        self.positioner = data_updater.positioner
        self.data_updater = data_updater

    def remove_special_placement_entry(self, letter: str, arrow: Arrow) -> None:
        orientation_key = self.data_updater._get_orientation_key(arrow.motion.start_ori)
        file_path = os.path.join(
            self.positioner.placement_manager.pictograph.main_widget.parent_directory,
            f"{orientation_key}/{letter}_placements.json",
        )

        if os.path.exists(file_path):
            data = self.data_updater.json_handler.load_json_data(file_path)
            if letter in data:
                letter_data = data[letter]
                turns_tuple = (
                    self.positioner.turns_tuple_generator.generate_turns_tuple(letter)
                )

                # Remove the primary entry
                self._remove_turn_data_entry(letter_data, turns_tuple, arrow)

                # Handle mirrored entry for Type 1 and Type 4 letters
                letter_type = LetterType.get_letter_type(letter)
                if letter_type in [Type1, Type4]:
                    mirrored_turns_tuple = self._generate_mirrored_tuple(
                        arrow, letter_type
                    )
                    if mirrored_turns_tuple:
                        self._remove_turn_data_entry(
                            letter_data, mirrored_turns_tuple, arrow
                        )

                self.data_updater.json_handler.write_json_data(data, file_path)
            arrow.pictograph.main_widget.refresh_placements()

    def _generate_mirrored_tuple(
        self, arrow: Arrow, letter_type: LetterType
    ) -> Union[str, None]:
        if letter_type == Type1:
            turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(
                arrow.pictograph.letter
            )
            items = turns_tuple.strip("()").split(", ")
            return f"({items[1]}, {items[0]})"
        elif letter_type == Type4:
            turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(
                arrow.pictograph.letter
            )
            prop_rotation = "cw" if "ccw" in turns_tuple else "ccw"
            turns = turns_tuple[turns_tuple.find(",") + 2 :]
            return f"({prop_rotation}, {turns}"
        return None

    def _remove_turn_data_entry(
        self, letter_data: dict, turns_tuple: str, arrow: Arrow, color: str = None
    ) -> None:
        turn_data = letter_data.get(turns_tuple, {})
        if arrow.motion.lead_state in turn_data:
            del turn_data[arrow.motion.lead_state]
            if not turn_data:
                del letter_data[turns_tuple]
        elif arrow.motion.motion_type in turn_data:
            del turn_data[arrow.motion.motion_type]
            if not turn_data:
                del letter_data[turns_tuple]
        elif color in turn_data:
            del turn_data[color]
            if not turn_data:
                del letter_data[turns_tuple]
