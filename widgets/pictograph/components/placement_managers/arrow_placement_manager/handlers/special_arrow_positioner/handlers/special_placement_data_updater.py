import os
import logging
from typing import TYPE_CHECKING, Union
from Enums import LetterType
from constants import IN, OUT, Type1
from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import Letters
from utilities.TypeChecking.letter_lists import Type1_non_hybrid_letters
from widgets.pictograph.components.placement_managers.arrow_placement_manager.handlers.special_arrow_positioner.handlers.mirrored_tuple_handler import (
    MirroredTupleHandler,
)
from widgets.pictograph.components.placement_managers.arrow_placement_manager.handlers.special_arrow_positioner.handlers.special_placement_entry_remover import (
    SpecialPlacementEntryRemover,
)
from widgets.pictograph.components.placement_managers.arrow_placement_manager.handlers.special_arrow_positioner.handlers.special_placement_json_handler import (
    SpecialPlacementJsonDataHandler,
)

if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Refactored SpecialPlacementDataUpdater
class SpecialPlacementDataUpdater:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner
        self.entry_remover = SpecialPlacementEntryRemover(self)

    def update_arrow_adjustments_in_json(
        self, adjustment: tuple[int, int], arrow: Arrow
    ) -> None:
        if not arrow:
            return

        letter = self.positioner.pictograph.letter
        turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(letter)
        orientation_key = self._get_orientation_key(arrow.motion.start_ori)

        letter_data = self._get_letter_data(letter, orientation_key)
        self._update_or_create_turn_data(letter_data, turns_tuple, arrow, adjustment)

        file_path = os.path.join(
            self.positioner.placement_manager.pictograph.main_widget.parent_directory,
            orientation_key,
            f"{letter}_placements.json",
        )
        existing_data = SpecialPlacementJsonDataHandler.load_json_data(file_path)
        existing_data[letter] = letter_data
        SpecialPlacementJsonDataHandler.write_json_data(existing_data, file_path)

        logging.info(
            f"Updated {letter} in {orientation_key} at {turns_tuple} with adjustment {adjustment}. Current values: {letter_data.get(turns_tuple)}"
        )

    def _get_letter_data(self, letter: str, orientation_key: str) -> dict:
        return (
            self.positioner.placement_manager.pictograph.main_widget.special_placements[
                orientation_key
            ].get(letter, {})
        )

    def _update_or_create_turn_data(
        self,
        letter_data: dict,
        turns_tuple: str,
        arrow: Arrow,
        adjustment: tuple[int, int],
    ) -> None:
        turn_data = letter_data.get(turns_tuple, {})
        key = self.positioner.motion_key_generator.generate_motion_key(arrow)

        if key in turn_data:
            turn_data[key][0] += adjustment[0]
            turn_data[key][1] += adjustment[1]
        else:
            default_adjustment = self._get_default_adjustment(arrow)
            turn_data[key] = [
                default_adjustment[0] + adjustment[0],
                default_adjustment[1] + adjustment[1],
            ]

        letter_data[turns_tuple] = turn_data

    def _get_default_adjustment(self, arrow: Arrow) -> tuple[int, int]:
        default_mgr = (
            self.positioner.pictograph.arrow_placement_manager.default_positioner
        )
        return default_mgr.get_default_adjustment(arrow)

    def _get_orientation_key(self, motion_start_ori) -> str:
        return "from_radial" if motion_start_ori in [IN, OUT] else "from_nonradial"

    def remove_special_placement_entry(self, letter: str, arrow: Arrow) -> None:
        self.entry_remover.remove_special_placement_entry(letter, arrow)

    def update_mirrored_entry_in_json(
        self, adjustment: tuple[int, int], arrow: "Arrow"
    ) -> None:
        if (
            not LetterType.get_letter_type(arrow.pictograph.letter) == Type1
            or arrow.pictograph.letter not in Type1_non_hybrid_letters
        ):
            return

        letter = self.positioner.pictograph.letter
        turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(letter)
        mirrored_turns_tuple = MirroredTupleHandler.mirror_turns_tuple(turns_tuple)
        if not mirrored_turns_tuple:
            return
        orientation_key = self._get_orientation_key(arrow.motion.start_ori)
        letter_data = (
            self.positioner.placement_manager.pictograph.main_widget.special_placements[
                orientation_key
            ].get(letter, {})
        )

        original_turn_data = letter_data.get(turns_tuple, {})
        existing_adjustment = original_turn_data.get(arrow.color, adjustment)

        mirrored_color = "blue" if arrow.color == "red" else "red"
        mirrored_turn_data = letter_data.get(mirrored_turns_tuple, {})
        mirrored_turn_data[mirrored_color] = existing_adjustment

        letter_data[mirrored_turns_tuple] = mirrored_turn_data
        self.positioner.placement_manager.pictograph.main_widget.special_placements[
            letter
        ] = letter_data
        self.update_specific_entry_in_json(letter, letter_data, arrow)

    def update_specific_entry_in_json(
        self, letter: Letters, letter_data: dict, object: Union[Arrow, Prop]
    ) -> None:
        try:
            orientation_key = self._get_orientation_key(object.motion.start_ori)
            base_directory = (
                self.positioner.placement_manager.pictograph.main_widget.parent_directory
            )
            file_path = os.path.join(
                base_directory, orientation_key, f"{letter}_placements.json"
            )

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            existing_data = SpecialPlacementJsonDataHandler.load_json_data(file_path)
            existing_data[letter] = letter_data

            SpecialPlacementJsonDataHandler.write_json_data(existing_data, file_path)
        except Exception as e:
            logging.error(f"Error in update_specific_entry_in_json: {e}")

    def _get_orientation_key(self, motion_start_ori) -> str:
        return "from_radial" if motion_start_ori in [IN, OUT] else "from_nonradial"
