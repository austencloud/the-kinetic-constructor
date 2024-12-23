import json
from Enums.letters import LetterConditions
from data.constants import (
    ANTI,
    BOX,
    DIAMOND,
    FLOAT,
    NONRADIAL,
    CLOCK,
    COUNTER,
    DASH,
    IN,
    OUT,
    PRO,
    RADIAL,
    STATIC,
)
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from .arrow_placement_manager import ArrowPlacementManager
import codecs


class DefaultArrowPositioner:
    def __init__(
        self, placement_manager: "ArrowPlacementManager", grid_mode: str = None
    ) -> None:
        self.placement_manager = placement_manager
        self.pictograph = placement_manager.pictograph
        self.diamond_placements_files = {
            PRO: "default_diamond_pro_placements.json",
            ANTI: "default_diamond_anti_placements.json",
            FLOAT: "default_diamond_float_placements.json",
            DASH: "default_diamond_dash_placements.json",
            STATIC: "default_diamond_static_placements.json",
        }
        self.box_placement_files = {
            PRO: "default_box_pro_placements.json",
            ANTI: "default_box_anti_placements.json",
            FLOAT: "default_box_float_placements.json",
            DASH: "default_box_dash_placements.json",
            STATIC: "default_box_static_placements.json",
        }
        self._load_all_default_placements(grid_mode)

    def _load_all_default_placements(self, grid_mode: str = None) -> None:
        self.default_placements = {}
        motion_types = [PRO, ANTI, FLOAT, DASH, STATIC]
        for motion_type in motion_types:
            self.default_placements[motion_type] = (
                self._load_default_placements_for_motion_type(motion_type, grid_mode)
            )

    def _load_default_placements_for_motion_type(
        self, motion_type: str, grid_mode: str = None
    ) -> dict[str, dict[str, list[int]]]:
        if not grid_mode:
            grid_mode = (
                self.placement_manager.pictograph.main_widget.settings_manager.global_settings.get_grid_mode()
            )
        if grid_mode == DIAMOND:
            json_filename = self.diamond_placements_files.get(motion_type)
            json_path = get_images_and_data_path(
                f"data/arrow_placement/diamond/default/{json_filename}"
            )
        elif grid_mode == BOX:
            json_filename = self.box_placement_files.get(motion_type)
            json_path = get_images_and_data_path(
                f"data/arrow_placement/box/default/{json_filename}"
            )
        with codecs.open(json_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _get_adjustment_key(self, arrow: Arrow, default_placements: dict) -> str:
        self._load_all_default_placements()

        has_beta_props = arrow.pictograph.check.ends_with_beta()
        has_alpha_props = arrow.pictograph.check.ends_with_alpha()
        has_gamma_props = arrow.pictograph.check.ends_with_gamma()
        has_hybrid_orientation = arrow.pictograph.check.ends_with_layer3()
        has_radial_props = arrow.pictograph.check.ends_with_radial_ori()
        has_nonradial_props = arrow.pictograph.check.ends_with_nonradial_ori()
        motion_end_ori = arrow.motion.end_ori

        key_suffix = "_to_"
        motion_end_ori_key = ""
        if has_hybrid_orientation:
            if motion_end_ori in [IN, OUT]:
                motion_end_ori_key = f"{RADIAL}_"
            elif motion_end_ori in [CLOCK, COUNTER]:
                motion_end_ori_key = f"{NONRADIAL}_"
        letter_suffix = ""
        if (
            arrow.pictograph.letter.value
            and (
                arrow.pictograph.letter
                in arrow.pictograph.letter.get_letters_by_condition(
                    LetterConditions.TYPE3
                )
            )
            or (
                arrow.pictograph.letter
                in arrow.pictograph.letter.get_letters_by_condition(
                    LetterConditions.TYPE5
                )
            )
        ):
            char = arrow.pictograph.letter.value[:-1]
            letter_suffix = f"_{char}_dash"

        elif arrow.pictograph.letter:
            letter_suffix = f"_{arrow.pictograph.letter.value}"

        if has_radial_props:
            key_middle = "layer1"
        elif has_nonradial_props:
            key_middle = "layer2"
        elif has_hybrid_orientation:
            key_middle = "layer3"
        if has_alpha_props:
            key_middle += "_alpha"
        elif has_beta_props:
            key_middle += "_beta"
        elif has_gamma_props:
            key_middle += "_gamma"

        key = arrow.motion.motion_type + (
            key_suffix + motion_end_ori_key + key_middle if key_middle else ""
        )
        key_with_letter = f"{key}{letter_suffix}"

        if key_with_letter in default_placements:
            return key_with_letter
        elif key in default_placements:
            return key
        else:
            return arrow.motion.motion_type

    def get_default_adjustment(self, arrow: Arrow) -> tuple[int, int]:
        if arrow.motion.motion_type in self.default_placements:
            default_placements = self.default_placements[arrow.motion.motion_type]
        else:
            default_placements = {}

        adjustment_key = self._get_adjustment_key(arrow, default_placements)

        if (
            adjustment_key in default_placements
            and str(arrow.motion.turns) in default_placements[adjustment_key]
        ):
            return default_placements[adjustment_key][str(arrow.motion.turns)]
        else:
            return default_placements.get(arrow.motion.motion_type, {}).get(
                str(arrow.motion.turns), (0, 0)
            )
