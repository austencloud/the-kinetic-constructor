import json
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING, Dict, List, Tuple


if TYPE_CHECKING:
    from objects.arrow.arrow_placement_manager.main_arrow_placement_manager import (
        MainArrowPlacementManager,
    )
    from objects.pictograph.pictograph import Pictograph


class DefaultArrowPlacementManager:
    def __init__(
        self,
        pictograph: "Pictograph",
        main_arrow_placement_manager: "MainArrowPlacementManager",
    ) -> None:
        self.pictograph = pictograph
        self.main_arrow_placement_manager = main_arrow_placement_manager
        self.letters_to_reposition = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            "Σ",
            "Δ",
            "θ",
            "Ω",
            "Φ",
            "Ψ",
            "Λ",
            "W-",
            "X-",
            "Y-",
            "Z-",
            "Σ-",
            "Δ-",
            "θ-",
            "Ω-",
            "Λ-",
        ]
        self.default_placement_letters = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            "Σ",
            "Δ",
            "θ",
            "Ω",
            "Φ",
            "Ψ",
            "Λ",
            "W-",
            "X-",
            "Y-",
            "Z-",
        ]

    def get_default_adjustment(self, arrow: Arrow) -> Tuple[int, int]:
        json_path = "arrow_placement/default_placements.json"
        with open(json_path, "r") as file:
            default_placements: Dict[str, Dict[str, List[int]]] = json.load(file)
        return default_placements.get(arrow.motion_type).get(str(arrow.turns))
