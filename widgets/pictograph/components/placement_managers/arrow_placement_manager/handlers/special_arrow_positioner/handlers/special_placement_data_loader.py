import json
import os
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner


class SpecialPlacementDataLoader:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner
        self.directory = "data/arrow_placement/special/"

    def load_placements(self) -> Dict:
        all_placements = {}
        for file_name in os.listdir(self.directory):
            if file_name.endswith("_placements.json"):
                with open(
                    os.path.join(self.directory, file_name),
                    "r",
                    encoding="utf-8",
                ) as file:
                    data = json.load(file)
                    all_placements.update(data)
        return all_placements
