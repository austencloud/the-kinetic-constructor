import os
import logging
from typing import TYPE_CHECKING, Union
from Enums import LetterType
from constants import IN, OUT, Type1, Type4, Type5
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.TypeChecking import Letters
from utilities.TypeChecking.letter_lists import Type1_non_hybrid_letters

if TYPE_CHECKING:
    from widgets.pictograph.components.placement_managers.arrow_placement_manager.handlers.special_arrow_positioner.handlers.special_placement_data_updater import (
        SpecialPlacementDataUpdater,
    )


class SpecialPlacementMirroredEntryHandler:
    """Handles mirrored special placement entries for Type 1 and Type 4 letters."""

    def __init__(self, data_updater: "SpecialPlacementDataUpdater") -> None:
        self.data_updater = data_updater

    def update_mirrored_entry_in_json(
        self, adjustment: tuple[int, int], arrow: "Arrow"
    ) -> None:
        letter_type = LetterType.get_letter_type(arrow.pictograph.letter)
        self._mirror_entry(adjustment, arrow, letter_type)
        self._update_pictographs_in_section(letter_type)

    def _mirror_entry(
        self, adjustment: tuple[int, int], arrow: "Arrow", letter_type: LetterType
    ) -> None:
        if letter_type in [Type1, Type4, Type5]:
            mirrored_color = (
                "blue"
                if arrow.color == "red"
                else "red"
                if letter_type == Type1
                else None
            )
            mirrored_turns_tuple = self._generate_mirrored_tuple(arrow, mirrored_color)
            if mirrored_turns_tuple:
                self._create_or_update_mirrored_entry(
                    arrow.pictograph.letter,
                    mirrored_turns_tuple,
                    adjustment,
                    arrow,
                    mirrored_color,
                )

    def _generate_mirrored_tuple(
        self, arrow: "Arrow", mirrored_color: str = None
    ) -> Union[str, None]:
        turns_tuple = self._generate_turns_tuple(arrow)
        letter_type = LetterType.get_letter_type(arrow.pictograph.letter)
        other_arrow = arrow.pictograph.get.other_arrow(arrow)
        if arrow.turns == other_arrow.turns:
            return

        if letter_type == Type1:
            items = turns_tuple.strip("()").split(", ")
            return f"({items[1]}, {items[0]})"
        elif letter_type == Type4:
            prop_rotation = "cw" if "ccw" in turns_tuple else "ccw"
            turns = turns_tuple[turns_tuple.find(",") + 2 :]
            return (
                f"({prop_rotation}, {turns}"
                if "cw" in turns_tuple or "ccw" in turns_tuple
                else None
            )
        elif letter_type == Type5:
            if arrow.turns > 0 and other_arrow.turns > 0:
                items = turns_tuple.strip("()").split(", ")
                return f"({items[0]}, {items[2]}, {items[1]})"
            elif arrow.turns > 0 or other_arrow.turns > 0:
                prop_rotation = "cw" if "ccw" in turns_tuple else "ccw"
                turns = turns_tuple[turns_tuple.find(",") + 2 : -1]
                return f"({prop_rotation}, {turns})"
        return None

    def _create_or_update_mirrored_entry(
        self,
        letter: str,
        mirrored_turns_tuple: str,
        adjustment: tuple[int, int],
        arrow: Arrow,
        color: str = None,
    ) -> None:
        orientation_key = self.data_updater._get_orientation_key(arrow.motion.start_ori)
        letter_data = self._get_letter_data(orientation_key, letter)

        original_turns_tuple = self._generate_turns_tuple(arrow)
        original_turn_data: dict = letter_data.get(original_turns_tuple)
        mirrored_turn_data: dict = letter_data.get(
            mirrored_turns_tuple, original_turn_data.copy()
        )

        if LetterType.get_letter_type(arrow.pictograph.letter) == Type5:
            other_arrow = arrow.pictograph.get.other_arrow(arrow)
            if arrow.turns > 0 and other_arrow.turns > 0:
                other_color = "blue" if arrow.color == "red" else "red"
                # Replace only the color-specific entries
                for key in list(mirrored_turn_data.keys()):
                    if arrow.color in key:
                        new_key = key.replace(arrow.color, other_color)
                        mirrored_turn_data[new_key] = mirrored_turn_data.pop(key)
                # Set the mirrored adjustment for the other color
                mirrored_turn_data[other_color] = original_turn_data.get(
                    arrow.color, self.data_updater._get_default_adjustment(arrow)
                )
            elif arrow.turns > 0 or other_arrow.turns > 0:  # Special Case for Type 5
                # Maintain the same color for the mirrored entry
                mirrored_turn_data[arrow.color] = original_turn_data.get(
                    arrow.color, self.data_updater._get_default_adjustment(arrow)
                )
        else:
            # For other types, use the provided color or default to arrow's color
            entry_color = color if color else arrow.color
            mirrored_turn_data[entry_color] = mirrored_turn_data.get(
                entry_color, adjustment
            )

        letter_data[mirrored_turns_tuple] = mirrored_turn_data
        self.data_updater.update_specific_entry_in_json(letter, letter_data, arrow)

    def _update_pictographs_in_section(self, letter_type: LetterType) -> None:
        for (
            pictograph
        ) in self.data_updater.positioner.pictograph.scroll_area.sections_manager.get_section(
            letter_type
        ).pictographs.values():
            pictograph.arrow_placement_manager.update_arrow_placements()

    def _get_letter_data(self, orientation_key: str, letter: str) -> dict:
        return self.data_updater.positioner.placement_manager.pictograph.main_widget.special_placements.get(
            orientation_key, {}
        ).get(
            letter, {}
        )

    def _generate_turns_tuple(self, arrow: "Arrow") -> str:
        return self.data_updater.positioner.turns_tuple_generator.generate_turns_tuple(
            arrow.pictograph.letter
        )
