
import json
from typing import TYPE_CHECKING, Dict
if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner


class SpecialPlacementDataLoader:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner
        self.json_path = "arrow_placement/special_placements.json"

    def load_placements(self) -> Dict:
        try:
            with open(self.json_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File not found: {self.json_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"JSON decoding error occurred: {e}")
            return {}


