import re
from typing import TYPE_CHECKING, Dict, Tuple, Union
from utilities.TypeChecking.letter_lists import Type1_letters
if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner


class DataSorter:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner

    def sort_entries(self) -> None:
        data = self.positioner.data_loader.load_placements()
        for letter, letter_data in data.items():
            sorted_data = self._sort_letter_data(letter_data)
            data[letter] = sorted_data
        self.positioner.data_updater.update_specific_entry(data)

    def _sort_letter_data(self, letter_data: Dict) -> Dict:
        def sort_key(item) -> Tuple[int, Union[int, float], Union[int, float]]:
            key = item[0]
            numbers = [
                float(num) if "." in num else int(num)
                for num in re.findall(r"\d+\.?\d*", key)
            ]
            char = re.search(r"[so]", key)

            if self.positioner.pictograph.letter in Type1_letters:
                return (numbers[0], numbers[1] if len(numbers) > 1 else float("inf"))
            elif char:
                char_priority = {"s": 1, "o": 2}.get(char.group(), 3)
                return (
                    char_priority,
                    numbers[0],
                    numbers[1] if len(numbers) > 1 else float("inf"),
                )
            else:
                return (0, numbers[0], numbers[1] if len(numbers) > 1 else float("inf"))

        return dict(sorted(letter_data.items(), key=sort_key))
