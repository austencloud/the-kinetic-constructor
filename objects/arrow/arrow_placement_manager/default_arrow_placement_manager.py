import json
from constants import ANTI, ANTIRADIAL, CLOCK, COUNTER, DASH, IN, OUT, PRO, RADIAL, STATIC
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING, Dict, List, Tuple

from utilities.TypeChecking.TypeChecking import OrientationTypes

if TYPE_CHECKING:
    from objects.arrow.arrow_placement_manager.main_arrow_placement_manager import (
        MainArrowPlacementManager,
    )
    from objects.pictograph.pictograph import Pictograph
import codecs


class DefaultArrowPlacementManager:
    def __init__(
        self,
        pictograph: "Pictograph",
        main_arrow_placement_manager: "MainArrowPlacementManager",
    ) -> None:
        self.pictograph = pictograph
        self.main_arrow_placement_manager = main_arrow_placement_manager
        self.motion_type_files = {
            PRO: "pro_placements.json",
            ANTI: "anti_placements.json",
            DASH: "dash_placements.json",
            STATIC: "static_placements.json",
        }

    def _load_default_placements(
        self, motion_type: str
    ) -> Dict[str, Dict[str, List[int]]]:
        json_filename = self.motion_type_files.get(
            motion_type, "default_placements.json"
        )
        json_path = f"arrow_placement/{json_filename}"
        with codecs.open(json_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _get_adjustment_key(self, arrow: Arrow) -> str:
        has_beta_props = arrow.pictograph.has_props_in_beta()
        has_alpha_props = arrow.pictograph.has_props_in_alpha()
        has_gamma_props = arrow.pictograph.has_props_in_gamma()
        has_hybrid_orientation = arrow.pictograph.has_hybrid_orientations()
        has_radial_props = arrow.pictograph.has_all_radial_props()
        has_antiradial_props = arrow.pictograph.has_all_antiradial_props()
        motion_end_ori = arrow.motion.end_ori
        
        key_suffix = "_to_"
        motion_end_ori_key: OrientationTypes = ""

        if motion_end_ori in [IN, OUT]:
            motion_end_ori_key = RADIAL
        elif motion_end_ori in [CLOCK, COUNTER]:
            motion_end_ori_key = ANTIRADIAL
            
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

        key = arrow.motion_type + (key_suffix + motion_end_ori_key + key_middle if key_middle else "")
        if key in self._load_default_placements(arrow.motion_type):
            return key
        else:
            return arrow.motion_type

    def get_default_adjustment(self, arrow: Arrow) -> Tuple[int, int]:
        motion_type_placements = self._load_default_placements(arrow.motion_type)
        adjustment_key = self._get_adjustment_key(arrow)

        if (
            adjustment_key in motion_type_placements
            and str(arrow.turns) in motion_type_placements[adjustment_key]
        ):
            return motion_type_placements[adjustment_key][str(arrow.turns)]
        else:
            return motion_type_placements.get(arrow.motion_type, {}).get(
                str(arrow.turns), (0, 0)
            )
