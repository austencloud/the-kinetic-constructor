import os
import logging
from typing import TYPE_CHECKING
from constants import BLUE, CLOCK, COUNTER, IN, OUT, RED, special_placements_parent_directory
from objects.arrow.arrow import Arrow
from objects.motion.motion import Motion
from utilities.TypeChecking.TypeChecking import Letters
from .special_placement_entry_remover import SpecialPlacementEntryRemover
from .special_placement_json_handler import SpecialPlacementJsonHandler
from .mirrored_entry_manager.mirrored_entry_manager import (
    SpecialPlacementMirroredEntryManager,
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
        self.mirrored_entry_manager = SpecialPlacementMirroredEntryManager(self)

    def _get_letter_data(self, letter: str, ori_key: str) -> dict:
        return (
            self.positioner.placement_manager.pictograph.main_widget.special_placements[
                ori_key
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
        key = self.positioner.attr_key_generator.get_key(arrow)

        if key in turn_data and turn_data[key] != {}:
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

    def get_ori_key(self, motion: Motion) -> str:
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

    def get_other_layer3_ori_key(self, ori_key: str) -> str:
        if ori_key == "from_layer3_blue1_red2":
            return "from_layer3_blue2_red1"
        elif ori_key == "from_layer3_blue2_red1":
            return "from_layer3_blue1_red2"

    def _update_placement_json_data(
        self, letter: str, letter_data: dict, ori_key: str
    ) -> None:
        file_path = os.path.join(
            special_placements_parent_directory,
            ori_key,
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
        turns_tuple = self.positioner.pictograph.main_widget.turns_tuple_generator.generate_turns_tuple(
            self.positioner.pictograph
        )
        ori_key = self.get_ori_key(arrow.motion)

        letter_data = self._get_letter_data(letter, ori_key)
        self._update_or_create_turn_data(letter_data, turns_tuple, arrow, adjustment)
        self._update_placement_json_data(letter, letter_data, ori_key)

        logging.info(
            f"Updated {letter} in {ori_key} at {turns_tuple} with adjustment {adjustment}. Current values: {letter_data.get(turns_tuple)}"
        )

    def update_specific_entry_in_json(
        self, letter: Letters, letter_data: dict, ori_key
    ) -> None:
        try:
            self._update_placement_json_data(letter, letter_data, ori_key)
        except Exception as e:
            logging.error(f"Error in update_specific_entry_in_json: {e}")
