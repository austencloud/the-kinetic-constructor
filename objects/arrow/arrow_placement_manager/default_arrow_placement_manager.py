import json
from constants import ANTI, DASH, PRO, STATIC
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING, Dict, List, Tuple

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

        if arrow.motion_type == STATIC:
            return "static_to_beta" if has_beta_props else STATIC
        elif arrow.motion_type in [DASH, PRO, ANTI]:
            key_suffix = "_to_"
            key_middle = ""
            if has_radial_props and has_beta_props:
                key_middle = "radial_beta"
            elif has_antiradial_props and has_beta_props:
                key_middle = "antiradial_beta"
            elif has_radial_props and has_alpha_props:
                key_middle = "radial_alpha"
            elif has_antiradial_props and has_alpha_props:
                key_middle = "antiradial_alpha"
            elif has_hybrid_orientation:
                key_middle = "hybrid_ori"
                if has_alpha_props:
                    key_middle += "_alpha"
                elif has_beta_props:
                    key_middle += "_beta"
                elif has_gamma_props:
                    key_middle += "_gamma"

            return arrow.motion_type + (key_suffix + key_middle if key_middle else "")
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
