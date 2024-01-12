import json
import re


class AdjustmentPersistenceManager:
    def __init__(self, pictograph) -> None:
        self.pictograph = pictograph
        self.json_path = "arrow_placement/special_placements.json"

    def save_json_data(self, data) -> None:
        with open(self.json_path, "w", encoding="utf-8") as file:
            json_str = json.dumps(data, indent=2, ensure_ascii=False)
            compact_json_str = re.sub(
                r'": \[\s+(-?\d+),\s+(-?\d+)\s+\]', r'": [\1, \2]', json_str
            )
            file.write(compact_json_str)

    def load_json_data(self) -> dict:
        with open(self.json_path, "r", encoding="utf-8") as file:
            return json.load(file)
