from typing import TYPE_CHECKING, Optional, Union
from Enums import LetterType
from constants import BLUE, RED, Type1, Type4, Type5, Type6
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.MotionAttributes import Colors, MotionTypes

if TYPE_CHECKING:
    from .special_placement_data_updater import SpecialPlacementDataUpdater


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
        if letter_type == Type1 and arrow.motion.motion_type != arrow.pictograph.get.other_motion(
            arrow.motion
        ).motion_type:
            mirrored_turns_tuple = self._generate_mirrored_tuple(arrow)
            if mirrored_turns_tuple:
                self._create_or_update_mirrored_entry(
                    arrow.pictograph.letter,
                    mirrored_turns_tuple,
                    arrow,
                )
            
        elif letter_type in [Type1, Type4, Type5, Type6]:
            mirrored_turns_tuple = self._generate_mirrored_tuple(arrow)
            if mirrored_turns_tuple:
                self._create_or_update_mirrored_entry(
                    arrow.pictograph.letter,
                    mirrored_turns_tuple,
                    arrow,
                )

    def _generate_mirrored_tuple(self, arrow: "Arrow") -> Union[str, None]:
        turns_tuple = self._generate_turns_tuple(arrow)
        letter_type = LetterType.get_letter_type(arrow.pictograph.letter)
        other_arrow = arrow.pictograph.get.other_arrow(arrow)
        if arrow.turns == other_arrow.turns:
            return None

        if letter_type == Type1 and arrow.motion.motion_type == arrow.pictograph.get.other_motion(
            arrow.motion
        ).motion_type:
            items = turns_tuple.strip("()").split(", ")
            return f"({items[1]}, {items[0]})"
        elif letter_type == Type4:
            prop_rotation = "cw" if "ccw" in turns_tuple else "ccw"
            turns = turns_tuple[turns_tuple.find(",") + 2 :]
            return (
                f"({prop_rotation}, {turns})"
                if "cw" in turns_tuple or "ccw" in turns_tuple
                else None
            )
        elif letter_type in [Type5, Type6]:
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
        arrow: Arrow,
    ) -> None:
        ori_key = self.data_updater._get_ori_key(arrow.motion)
        letter_data = self._get_letter_data(ori_key, letter)

        original_turns_tuple = self._generate_turns_tuple(arrow)
        original_turn_data: dict = letter_data.get(original_turns_tuple)
        mirrored_turn_data = {}

        default_adjustment = self.data_updater.positioner.placement_manager.default_positioner.get_default_adjustment(
            arrow
        )

        if LetterType.get_letter_type(arrow.pictograph.letter) in [Type5, Type6]:
            other_arrow = arrow.pictograph.get.other_arrow(arrow)
            if arrow.turns > 0 and other_arrow.turns > 0:
                other_color = "blue" if arrow.color == "red" else "red"
                for key in list(original_turn_data.keys()):
                    if arrow.color in key:
                        new_key = key.replace(arrow.color, other_color)
                        mirrored_turn_data[other_color] = default_adjustment
                mirrored_turn_data[other_color] = original_turn_data.get(
                    arrow.color, self.data_updater._get_default_adjustment(arrow)
                )
            elif (
                arrow.turns > 0 or other_arrow.turns > 0
            ): 
                mirrored_turn_data[arrow.color] = original_turn_data.get(
                    arrow.color, self.data_updater._get_default_adjustment(arrow)
                )
        else:
            if arrow.pictograph.check.starts_from_mixed_orientation():
                other_ori_key = self.data_updater.get_other_layer3_ori_key(
                    ori_key
                )
                other_letter_data = self._get_letter_data(
                    other_ori_key, letter
                )
                if arrow.pictograph.check.has_hybrid_motions():
                    for key in list(original_turn_data.keys()):
                        mirrored_turn_data[key] = default_adjustment
                elif not arrow.pictograph.check.has_hybrid_motions():
                    key = RED if arrow.color == BLUE else BLUE
                    mirrored_turn_data[key] = original_turn_data[arrow.color]

            other_letter_data[mirrored_turns_tuple] = mirrored_turn_data
            self.data_updater.update_specific_entry_in_json(letter, other_letter_data, other_ori_key)
            return


        rotation_angle_override = self._check_for_rotation_angle_override(
            original_turn_data
        )
        if rotation_angle_override is not None:
            mirrored_turn_data[f"{other_color}_rot_angle"] = rotation_angle_override

        self.data_updater.update_specific_entry_in_json(letter, letter_data, ori_key)

    def _check_for_rotation_angle_override(self, turn_data: dict) -> Optional[int]:
        for key in turn_data.keys():
            if "rot_angle" in key:
                return turn_data[key]
        return None

    def _update_pictographs_in_section(self, letter_type: LetterType) -> None:
        section = self.data_updater.positioner.pictograph.scroll_area.sections_manager.get_section(
            letter_type
        )
        for pictograph in section.pictographs.values():
            pictograph.arrow_placement_manager.update_arrow_placements()

    def _get_letter_data(self, ori_key: str, letter: str) -> dict:
        return self.data_updater.positioner.placement_manager.pictograph.main_widget.special_placements.get(
            ori_key, {}
        ).get(
            letter, {}
        )

    def _generate_turns_tuple(self, arrow: "Arrow") -> str:
        return self.data_updater.positioner.turns_tuple_generator.generate_turns_tuple(
            arrow.pictograph.letter
        )
