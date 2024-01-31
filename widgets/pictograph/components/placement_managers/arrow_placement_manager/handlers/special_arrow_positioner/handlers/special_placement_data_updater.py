import os
import logging
from typing import TYPE_CHECKING, Union
from constants import BLUE, CLOCK, COUNTER, IN, OUT, RED
from objects.arrow.arrow import Arrow
from objects.motion.motion import Motion
from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import Letters
from .special_placement_entry_remover import SpecialPlacementEntryRemover
from .special_placement_json_handler import SpecialPlacementJsonHandler
from .special_placement_mirrored_entry_handler import (
    SpecialPlacementMirroredEntryHandler,
)

if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class SpecialPlacementDataUpdater:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner
        self.json_handler = SpecialPlacementJsonHandler()
        self.entry_remover = SpecialPlacementEntryRemover(self)
        self.mirrored_entry_handler = SpecialPlacementMirroredEntryHandler(self)

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

    def _get_orientation_key(self, motion: Motion) -> str:
        other_motion = self.positioner.pictograph.get.other_motion(motion)
        if motion.start_ori in [IN, OUT] and other_motion.start_ori in [IN, OUT]:
            return "from_layer1"
        elif motion.start_ori in [CLOCK, COUNTER] and other_motion.start_ori in [
            CLOCK,
            COUNTER,
        ]:
            return "from_layer2"
        elif (
            motion.color == RED
            and motion.start_ori in [IN, OUT]
            and other_motion.start_ori in [CLOCK, COUNTER]
        ):
            return "from_layer3_blue2_red1"
        elif (
            motion.color == RED
            and motion.start_ori in [CLOCK, COUNTER]
            and other_motion.start_ori in [IN, OUT]
        ):
            return "from_layer3_blue1_red2"
        elif (
            motion.color == BLUE
            and motion.start_ori in [IN, OUT]
            and other_motion.start_ori in [CLOCK, COUNTER]
        ):
            return "from_layer3_blue1_red2"
        elif (
            motion.color == BLUE
            and motion.start_ori in [CLOCK, COUNTER]
            and other_motion.start_ori in [IN, OUT]
        ):
            return "from_layer3_blue2_red1"

    def _update_placement_json_data(
        self, letter: str, letter_data: dict, orientation_key: str
    ) -> None:
        file_path = os.path.join(
            self.positioner.placement_manager.pictograph.main_widget.parent_directory,
            orientation_key,
            f"{letter}_placements.json",
        )
        existing_data = self.json_handler.load_json_data(file_path)
        existing_data[letter] = letter_data
        self.json_handler.write_json_data(existing_data, file_path)

    def update_arrow_adjustments_in_json(
        self, adjustment: tuple[int, int], arrow: Arrow
    ) -> None:
        if not arrow:
            return

        letter = self.positioner.pictograph.letter
        turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(letter)
        orientation_key = self._get_orientation_key(arrow.motion)

        letter_data = self._get_letter_data(letter, orientation_key)
        self._update_or_create_turn_data(letter_data, turns_tuple, arrow, adjustment)
        self._update_placement_json_data(letter, letter_data, orientation_key)

        logging.info(
            f"Updated {letter} in {orientation_key} at {turns_tuple} with adjustment {adjustment}. Current values: {letter_data.get(turns_tuple)}"
        )

    def update_specific_entry_in_json(
        self, letter: Letters, letter_data: dict, object: Union[Arrow, Prop]
    ) -> None:
        try:
            orientation_key = self._get_orientation_key(object.motion)
            self._update_placement_json_data(letter, letter_data, orientation_key)
        except Exception as e:
            logging.error(f"Error in update_specific_entry_in_json: {e}")
