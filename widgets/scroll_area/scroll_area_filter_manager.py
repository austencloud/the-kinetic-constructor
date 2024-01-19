from typing import TYPE_CHECKING, Dict, List, Union

from utilities.TypeChecking.TypeChecking import Turns, Orientations

if TYPE_CHECKING:
    from .scroll_area import ScrollArea

class ScrollAreaFilterTabManager:
    def __init__(self, scroll_area: "ScrollArea") -> None:
        self.scroll_area = scroll_area
        self.filters: Dict[str, Union[Turns, Orientations]] = {}

    def filter_pictographs(self, pictograph_dicts: List[Dict]) -> List[Dict]:
        return [
            pictograph_dict
            for pictograph_dict in pictograph_dicts
            if self.pictograph_matches_filters(pictograph_dict)
        ]

    def pictograph_matches_filters(self, pictograph_dict: Dict) -> bool:
        for filter_key, filter_value in self.filters.items():
            if filter_value in ["0", "1", "2", "3"]:
                filter_value = int(filter_value)
            elif filter_value in ["0.5", "1.5", "2.5"]:
                filter_value = float(filter_value)
            if filter_value != "":
                if pictograph_dict.get(filter_key) != filter_value:
                    return False
        return True

