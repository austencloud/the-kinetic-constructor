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
        if letter_type == Type1:
            self._mirror_entry_for_type1(adjustment, arrow)
        elif letter_type == Type4:
            self._mirror_entry_for_type4(adjustment, arrow)
        elif letter_type == Type5:
            self._mirror_entry_for_type5(adjustment, arrow)

        self._update_pictographs_in_section(letter_type)

    def _mirror_entry_for_type1(
        self, adjustment: tuple[int, int], arrow: "Arrow"
    ) -> None:
        if (
            arrow.pictograph.letter not in Type1_non_hybrid_letters
            or arrow.pictograph.letter in ["S", "T"]
        ):
            return
        mirrored_turns_tuple = self._generate_type1_mirrored_tuple(arrow)
        if mirrored_turns_tuple:
            mirrored_color = "blue" if arrow.color == "red" else "red"
            self._create_or_update_mirrored_entry(
                arrow.pictograph.letter,
                mirrored_turns_tuple,
                adjustment,
                arrow,
                mirrored_color,
            )

    def _mirror_entry_for_type5(self, adjustment: tuple[int, int], arrow: Arrow) -> None:
        mirrored_turns_tuple = self._generate_type5_mirrored_tuple(arrow)
        if mirrored_turns_tuple:
            self._create_or_update_mirrored_entry_for_type5(
                arrow.pictograph.letter,
                mirrored_turns_tuple,
                adjustment,
                arrow
            )

    def _generate_type5_mirrored_tuple(self, arrow: Arrow) -> Union[str, None]:
        turns_tuple = self._generate_turns_tuple(arrow)
        items = turns_tuple.strip("()").split(", ")
        return f"({items[0]}, {items[2]}, {items[1]})"

    def _mirror_entry_for_type4(
        self, adjustment: tuple[int, int], arrow: "Arrow"
    ) -> None:
        mirrored_turns_tuple = self._generate_type4_mirrored_prop_rotation(arrow)
        if mirrored_turns_tuple:
            self._create_or_update_mirrored_entry(
                arrow.pictograph.letter, mirrored_turns_tuple, adjustment, arrow
            )

    def _generate_type4_mirrored_prop_rotation(
        self, arrow: "Arrow"
    ) -> Union[str, None]:
        turns_tuple = self._generate_turns_tuple(arrow)
        prop_rotation = "cw" if "ccw" in turns_tuple else "ccw"
        turns = turns_tuple[turns_tuple.find(",") + 2 :]
        return (
            f"({prop_rotation}, {turns}"
            if "cw" in turns_tuple or "ccw" in turns_tuple
            else None
        )

    def _generate_type1_mirrored_tuple(self, arrow: "Arrow") -> Union[str, None]:
        turns_tuple = self._generate_turns_tuple(arrow)
        items = turns_tuple.strip("()").split(", ")
        return f"({items[1]}, {items[0]})"

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

        original_turn_data = letter_data.get(self._generate_turns_tuple(arrow), {})

        if mirrored_turns_tuple not in letter_data:
            mirrored_turn_data = original_turn_data.copy()
            mirrored_turn_data[color if color else arrow.color] = adjustment
        else:
            mirrored_turn_data = letter_data[mirrored_turns_tuple]
            mirrored_turn_data[
                color if color else arrow.color
            ] = mirrored_turn_data.get(color if color else arrow.color, adjustment)

        letter_data[mirrored_turns_tuple] = mirrored_turn_data
        self.data_updater.update_specific_entry_in_json(letter, letter_data, arrow)


    def _create_or_update_mirrored_entry_for_type5(
        self,
        letter: str,
        mirrored_turns_tuple: str,
        adjustment: tuple[int, int],
        arrow: Arrow
    ) -> None:
        orientation_key = self.data_updater._get_orientation_key(arrow.motion.start_ori)
        letter_data = self._get_letter_data(orientation_key, letter)

        original_turn_data = letter_data.get(self._generate_turns_tuple(arrow), {})
        mirrored_turn_data = letter_data.get(mirrored_turns_tuple, {})

        other_color = "blue" if arrow.color == "red" else "red"

        # If mirrored entry does not exist, copy the original and replace with the opposite color
        if not mirrored_turn_data:
            mirrored_turn_data = original_turn_data.copy()
            if arrow.color in mirrored_turn_data:
                del mirrored_turn_data[arrow.color]

        mirrored_turn_data[other_color] = original_turn_data.get(arrow.color, adjustment)
        
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
