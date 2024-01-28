import os
import logging
from typing import TYPE_CHECKING, Union
from Enums import LetterType
from constants import IN, OUT, Type1
from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import Letters
from utilities.TypeChecking.letter_lists import Type1_non_hybrid_letters

if TYPE_CHECKING:
    from widgets.pictograph.components.placement_managers.arrow_placement_manager.handlers.special_arrow_positioner.handlers.special_placement_data_updater import (
        SpecialPlacementDataUpdater,
    )


class SpecialPlacementMirroredEntryHandler:
    def __init__(self, data_updater: "SpecialPlacementDataUpdater") -> None:
        self.data_updater = data_updater

    def update_mirrored_entry_in_json(
        self, adjustment: tuple[int, int], arrow: "Arrow"
    ) -> None:
        if (
            not LetterType.get_letter_type(arrow.pictograph.letter) == Type1
            or arrow.pictograph.letter not in Type1_non_hybrid_letters
        ):
            return

        letter = self.data_updater.positioner.pictograph.letter
        turns_tuple = (
            self.data_updater.positioner.turns_tuple_generator.generate_turns_tuple(
                letter
            )
        )
        mirrored_turns_tuple = self.mirror_turns_tuple(turns_tuple)
        if not mirrored_turns_tuple:
            return
        orientation_key = self.data_updater._get_orientation_key(arrow.motion.start_ori)
        letter_data = self.data_updater.positioner.placement_manager.pictograph.main_widget.special_placements[
            orientation_key
        ].get(
            letter, {}
        )

        original_turn_data = letter_data.get(turns_tuple, {})
        existing_adjustment = original_turn_data.get(arrow.color, adjustment)

        mirrored_color = "blue" if arrow.color == "red" else "red"
        mirrored_turn_data = letter_data.get(mirrored_turns_tuple, {})
        mirrored_turn_data[mirrored_color] = existing_adjustment

        letter_data[mirrored_turns_tuple] = mirrored_turn_data
        self.data_updater.positioner.placement_manager.pictograph.main_widget.special_placements[
            letter
        ] = letter_data
        self.data_updater.update_specific_entry_in_json(letter, letter_data, arrow)

    @staticmethod
    def mirror_turns_tuple(turns_tuple: str) -> Union[str, None]:
        x, y = turns_tuple.strip("()").split(", ")
        if x != y:
            return f"({y}, {x})"
        return None
