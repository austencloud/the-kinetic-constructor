import os
from typing import TYPE_CHECKING, Union
from Enums import LetterType
from constants import BLUE, CLOCK, COUNTER, IN, OUT, RED, Type1, Type4, Type5
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.MotionAttributes import Colors
from utilities.TypeChecking.letter_lists import Type1_hybrid_letters

if TYPE_CHECKING:
    from .special_placement_data_updater import SpecialPlacementDataUpdater


class SpecialPlacementEntryRemover:
    """Handles removal of special placement entries."""

    def __init__(
        self,
        data_updater: "SpecialPlacementDataUpdater",
    ) -> None:
        self.positioner = data_updater.positioner
        self.data_updater = data_updater

    def remove_special_placement_entry(self, letter: str, arrow: Arrow) -> None:
        ori_key = self.data_updater._get_ori_key(arrow.motion)
        file_path = os.path.join(
            self.positioner.placement_manager.pictograph.main_widget.parent_directory,
            f"{ori_key}/{letter}_placements.json",
        )
        if os.path.exists(file_path):
            data = self.data_updater.json_handler.load_json_data(file_path)
            if letter in data:
                letter_data = data[letter]
                turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(letter)
                self._remove_turn_data_entry(letter_data, turns_tuple, arrow, arrow.color)

                letter_type = LetterType.get_letter_type(letter)
                mirrored_turns_tuple = self._generate_mirrored_tuple(arrow, letter_type)
                if mirrored_turns_tuple:
                    other_arrow = arrow.pictograph.get.other_arrow(arrow)
                    color_for_removal = arrow.color

                    # Check if it's the special Type 5 edge case
                    if letter_type == Type5 and (arrow.turns > 0 or other_arrow.turns > 0):
                        if not (arrow.turns > 0 and other_arrow.turns > 0):
                            # If one arrow has turns and the other doesn't, keep the same color
                            color_for_removal = arrow.color
                    else:
                        color_for_removal = self._get_other_color(arrow.color)

                    self._remove_turn_data_entry(letter_data, mirrored_turns_tuple, arrow, color_for_removal)

                self.data_updater.json_handler.write_json_data(data, file_path)
            arrow.pictograph.main_widget.refresh_placements()

    def _get_other_color(self, color: Colors) -> Colors:
        return RED if color == BLUE else BLUE

    def _generate_mirrored_tuple(
        self, arrow: Arrow, letter_type: LetterType
    ) -> Union[str, None]:
        turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(
            arrow.pictograph.letter
        )

        if letter_type in [Type1, Type4]:
            items = turns_tuple.strip("()").split(", ")
            prop_rotation = "cw" if "ccw" in turns_tuple else "ccw"
            return f"({prop_rotation}, {items[1]})" if letter_type == Type4 else f"({items[1]}, {items[0]})"

        elif letter_type == Type5:
            other_arrow = arrow.pictograph.get.other_arrow(arrow)
            items = turns_tuple.strip("()").split(", ")
            # Check if one arrow has turns and the other does not
            if arrow.turns > 0 and other_arrow.turns > 0:
                return f"({items[0]}, {items[2]}, {items[1]})"
            elif arrow.turns > 0 or other_arrow.turns > 0:
                prop_rotation = "cw" if "ccw" in turns_tuple else "ccw"
                turns = turns_tuple[turns_tuple.find(",") + 2 : -1]
                return f"({prop_rotation}, {turns})"

        return None

    def _remove_turn_data_entry(self, letter_data: dict, turns_tuple: str, arrow: Arrow, color: str) -> None:
        key = self._generate_key_for_removal(arrow)
        turn_data = letter_data.get(turns_tuple, {})
        if key in turn_data:
            del turn_data[key]
            if not turn_data:
                del letter_data[turns_tuple]

    def _generate_key_for_removal(self, arrow: Arrow) -> str:
        if arrow.pictograph.check.starts_from_mixed_orientation():
            if arrow.motion.start_ori in [IN, OUT]:
                layer = "layer1" 
            elif arrow.motion.start_ori in [CLOCK, COUNTER]:
                layer = "layer2"
            return f"{arrow.motion.motion_type}_from_{layer}"
        elif arrow.pictograph.letter in Type1_hybrid_letters:
            return arrow.motion.motion_type
        return arrow.color
