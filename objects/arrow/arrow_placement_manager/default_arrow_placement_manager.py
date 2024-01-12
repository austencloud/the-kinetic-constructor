import json
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


    def get_default_adjustment(self, arrow: Arrow) -> Tuple[int, int]:
        json_path = "arrow_placement/default_placements.json"
        with codecs.open(json_path, "r", encoding="utf-8") as file:
            default_placements: Dict[str, Dict[str, List[int]]] = json.load(file)
        return default_placements.get(arrow.motion_type).get(str(arrow.turns))
