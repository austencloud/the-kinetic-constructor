import json
from typing import Dict, List, Tuple, Union
from constants import (
    ANTI,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    NORTHEAST,
    NORTHWEST,
    PRO,
    SOUTHEAST,
    SOUTHWEST,
)



class Generate_I_Adjustments:
    def __init__(self) -> None:
        self.adjustment_values = {
            (0, 0): [(75, -85), (50, -25)],
            (0, 0.5): [(50, -35), (-110, -115)],
            (0, 1): [(75, -85), (50, -25)],
            (0, 1.5): [(75, -80), (-65, -30)],
            (0, 2): [(75, -85), (50, -25)],
            (0, 2.5): [(50, -35), (-90, 110)],
            (0, 3): [(75, -85), (50, -25)],
            (0.5, 0): [(-15, 55), (75, -70)],
            (0.5, 0.5): [(5, 40), (-60, 115)],
            (0.5, 1): [(-15, 55), (75, -70)],
            (0.5, 1.5): [(30, 90), (-15, -35)],
            (0.5, 2): [(-15, 55), (75, -70)],
            (0.5, 2.5): [(5, 55), (-60, 110)],
            (0.5, 3): [(-15, 55), (75, -70)],
            (1, 0): [(70, -90), (65, -70)],
            (1, 0.5): [(55, -50), (-85, 115)],
            (1, 1): [(5, -50), (55, -15)],
            (1, 1.5): [(-45, -65), (-70, 20)],
            (1, 2): [(5, -50), (55, -15)],
            (1, 2.5): [(-10, 5), (-85, 115)],
            (1, 3): [(5, -50), (55, -15)],
            (1.5, 0): [(15, 5), (-80, 70)],
            (1.5, 0.5): [(-10, 5), (-80, 130)],
            (1.5, 1): [(15, 5), (-80, 70)],
            (1.5, 1.5): [(-30, 25), (-50, -45)],
            (1.5, 2): [(15, 5), (-80, 70)],
            (1.5, 2.5): [(-10, 5), (-75, 130)],
            (1.5, 3): [(15, 5), (-80, 70)],
            (2, 0): [(70, -90), (50, -20)],
            (2, 0.5): [(55, -50), (-75, 120)],
            (2, 1): [(85, -105), (50, -20)],
            (2, 1.5): [(70, -40), (-50, -15)],
            (2, 2): [(80, -100), (45, -40)],
            (2, 2.5): [(55, -45), (-75, 130)],
            (2, 3): [(100, -85), (45, -30)],
            (2.5, 0): [(-5, 45), (-1, 40)],
            (2.5, 0.5): [(25, 50), (-75, 120)],
            (2.5, 1): [(-15, 60), (75, -70)],
            (2.5, 1.5): [(70, 65), (-60, -20)],
            (2.5, 2): [(-15, 60), (75, -70)],
            (2.5, 2.5): [(25, 45), (-60, 115)],
            (2.5, 3): [(-15, 60), (75, -70)],
            (3, 0): [(70, -90), (20, -50)],
            (3, 0.5): [(60, -45), (-80, 130)],
            (3, 1): [(85, -105), (20, -50)],
            (3, 1.5): [(70, -40), (-60, 20)],
            (3, 2): [(80, -100), (40, -45)],
            (3, 2.5): [(55, -45), (-75, 130)],
            (3, 3): [(100, -85), (30, -45)],
        }
        self.generate_and_save_settings("arrow_adjuster/I_adjustments.json")
        
    def generate_directional_tuples(
        self, x, y, ccw=False
    ) -> List[Tuple[Union[int, float], Union[int, float]]]:
        if ccw:
            # Corrected handling of negatives for 'ccw'
            return [(-y, -x), (x, -y), (y, x), (-x, y)]
        else:
            return [(x, y), (-y, x), (-x, -y), (y, -x)]

    def create_direction_dict_json(self, ne, se, sw, nw) -> Dict:
        return {
            NORTHEAST: list(ne),
            SOUTHEAST: list(se),
            SOUTHWEST: list(sw),
            NORTHWEST: list(nw),
        }

    def create_motion_type_dict_json(self, pro_values, anti_values) -> Dict:
        return {
            PRO: {
                CLOCKWISE: self.create_direction_dict_json(*pro_values[0]),
                COUNTER_CLOCKWISE: self.create_direction_dict_json(*pro_values[1]),
            },
            ANTI: {
                CLOCKWISE: self.create_direction_dict_json(*anti_values[0]),
                COUNTER_CLOCKWISE: self.create_direction_dict_json(*anti_values[1]),
            },
        }

    def generate_adjustments_as_dict(self) -> dict:
        adjustments_dict = {}
        for (pro_turns, anti_turns), base_values in self.adjustment_values.items():
            pro_turns_formatted = int(pro_turns) if pro_turns.is_integer() else pro_turns
            anti_turns_formatted = int(anti_turns) if anti_turns.is_integer() else anti_turns

            key = (pro_turns_formatted, anti_turns_formatted)
            adjustments_dict[str(key)] = {}

            for motion_type in [PRO, ANTI]:
                x, y = base_values[0 if motion_type == PRO else 1]
                adjustments_dict[str(key)][motion_type] = [x, y]

        return adjustments_dict

    def generate_and_save_settings(self, filename: str) -> None:
        adjustments_dict = self.generate_adjustments_as_dict()
        with open(filename, 'w') as file:
            json.dump(adjustments_dict, file, indent=4)

Generate_I_Adjustments()
