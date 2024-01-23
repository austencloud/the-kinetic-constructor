import json
from constants import (
    ANTI,
    ANTIRADIAL,
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
from typing import TYPE_CHECKING, Dict, List, Tuple
from utilities.TypeChecking.letter_lists import dash_letters
from utilities.TypeChecking.TypeChecking import OrientationTypes

if TYPE_CHECKING:
    from ..arrow_placement_manager import ArrowPlacementManager
import codecs


class DefaultArrowPositioner:
    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.placement_manager = placement_manager
        self.motion_type_files = {
            PRO: "pro_placements.json",
            ANTI: "anti_placements.json",
            DASH: "dash_placements.json",
            STATIC: "static_placements.json",
        }

    def _load_default_placements(
        self, motion_type: str
    ) -> Dict[str, Dict[str, List[int]]]:
        json_filename = self.motion_type_files.get(motion_type)
        json_path = f"data/arrow_placement/default/{json_filename}"
        with codecs.open(json_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _get_adjustment_key(self, arrow: Arrow) -> str:
        has_beta_props = arrow.pictograph.check.has_props_in_beta()
        has_alpha_props = arrow.pictograph.check.has_props_in_alpha()
        has_gamma_props = arrow.pictograph.check.has_props_in_gamma()
        has_hybrid_orientation = arrow.pictograph.check.has_hybrid_orientations()
        has_radial_props = arrow.pictograph.check.has_all_radial_props()
        has_antiradial_props = arrow.pictograph.check.has_all_antiradial_props()
        motion_end_ori = arrow.motion.end_ori

        key_suffix = "_to_"
        motion_end_ori_key: OrientationTypes = ""
        if has_hybrid_orientation:
            if motion_end_ori in [IN, OUT]:
                motion_end_ori_key = f"{RADIAL}_"
            elif motion_end_ori in [CLOCK, COUNTER]:
                motion_end_ori_key = f"{ANTIRADIAL}_"
        letter_suffix = ""
        if arrow.pictograph.letter and arrow.pictograph.letter in dash_letters:
            char = arrow.pictograph.letter[:-1]
            letter_suffix = f"_{char}_dash"
        elif arrow.pictograph.letter:
            letter_suffix = f"_{arrow.pictograph.letter}"

        if has_radial_props:
            key_middle = "layer1"
        elif has_antiradial_props:
            key_middle = "layer2"
        elif has_hybrid_orientation:
            key_middle = "layer3"
        if has_alpha_props:
            key_middle += "_alpha"
        elif has_beta_props:
            key_middle += "_beta"
        elif has_gamma_props:
            key_middle += "_gamma"

        default_placements = self._load_default_placements(arrow.motion.motion_type)
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

    def get_default_adjustment(self, arrow: Arrow) -> Tuple[int, int]:
        motion_type_placements = self._load_default_placements(arrow.motion.motion_type)
        adjustment_key = self._get_adjustment_key(arrow)

        if (
            adjustment_key in motion_type_placements
            and str(arrow.turns) in motion_type_placements[adjustment_key]
        ):
            return motion_type_placements[adjustment_key][str(arrow.turns)]
        else:
            return motion_type_placements.get(arrow.motion.motion_type, {}).get(
                str(arrow.turns), (0, 0)
            )
