import json
from PyQt6.QtCore import QPointF
from typing import Dict, Tuple


class ArrowAdjuster:
    def __init__(self, settings_file: str):
        self.settings_file = settings_file
        self.settings = self._load_settings()

    def _load_settings(self) -> Dict[Tuple[float, float], Dict]:
        try:
            with open(self.settings_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def get_adjustment(
        self,
        pro_turns: float,
        anti_turns: float,
        motion_type: str,
        prop_rot_dir: str,
        loc: str,
    ) -> QPointF:
        adjustment_key = (pro_turns, anti_turns)
        motion_type_adjustments = self.settings.get(str(adjustment_key), {}).get(
            motion_type, {}
        )
        direction_adjustments = motion_type_adjustments.get(prop_rot_dir, {})
        return QPointF(*direction_adjustments.get(loc, (0, 0)))

    def set_adjustment(
        self,
        pro_turns: float,
        anti_turns: float,
        motion_type: str,
        prop_rot_dir: str,
        loc: str,
        adjustment: Tuple[float, float],
    ):
        adjustment_key = (pro_turns, anti_turns)
        if str(adjustment_key) not in self.settings:
            self.settings[str(adjustment_key)] = {}
        if motion_type not in self.settings[str(adjustment_key)]:
            self.settings[str(adjustment_key)][motion_type] = {}
        if prop_rot_dir not in self.settings[str(adjustment_key)][motion_type]:
            self.settings[str(adjustment_key)][motion_type][prop_rot_dir] = {}
        self.settings[str(adjustment_key)][motion_type][prop_rot_dir][loc] = adjustment
        self._save_settings()

    def _save_settings(self):
        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file, indent=4)
