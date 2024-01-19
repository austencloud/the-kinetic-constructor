import json
from typing import TYPE_CHECKING, Dict
if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner

class SpecialPlacementDataUpdater:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner
        
    def update_specific_entry(
        self, letter: str, adjustment_key: str, new_data: Dict
    ) -> None:
        data = self.positioner.data_loader.load_placements()
        data.setdefault(letter, {})[adjustment_key] = new_data
        with open(self.positioner.data_loader.json_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


