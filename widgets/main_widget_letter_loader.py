from typing import TYPE_CHECKING, Dict, List
import pandas as pd
from constants import (
    BLUE_END_LOC,
    BLUE_MOTION_TYPE,
    BLUE_PROP_ROT_DIR,
    BLUE_START_LOC,
    BLUE_START_ORI,
    BLUE_TURNS,
    END_POS,
    IN,
    LETTER,
    RED_END_LOC,
    RED_MOTION_TYPE,
    RED_PROP_ROT_DIR,
    RED_START_LOC,
    RED_START_ORI,
    RED_TURNS,
    START_POS,
)
from utilities.TypeChecking.TypeChecking import Letters

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class MainLetterLoader:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget

    def load_all_letters(self) -> Dict[Letters, List[Dict]]:
        df: pd.Series = pd.read_csv("PictographDataframe.csv")
        df = df.sort_values(by=[LETTER, START_POS, END_POS])
        df = self.add_turns_and_ori_to_pictograph_dict(df)
        letters = (
            df.groupby(LETTER).apply(lambda x: x.to_dict(orient="records")).to_dict()
        )
        return letters

    def add_turns_and_ori_to_pictograph_dict(self, pictograph_dict) -> Dict:
        pictograph_dict = pictograph_dict[
            [
                LETTER,
                START_POS,
                END_POS,
                BLUE_MOTION_TYPE,
                BLUE_PROP_ROT_DIR,
                BLUE_START_LOC,
                BLUE_END_LOC,
                RED_MOTION_TYPE,
                RED_PROP_ROT_DIR,
                RED_START_LOC,
                RED_END_LOC,
            ]
        ]
        pictograph_dict[BLUE_TURNS] = 0
        pictograph_dict[RED_TURNS] = 0
        pictograph_dict[BLUE_START_ORI] = IN
        pictograph_dict[RED_START_ORI] = IN

        pictograph_dict = pictograph_dict[
            [
                LETTER,
                START_POS,
                END_POS,
                BLUE_MOTION_TYPE,
                BLUE_PROP_ROT_DIR,
                BLUE_START_LOC,
                BLUE_END_LOC,
                BLUE_START_ORI,
                BLUE_TURNS,
                RED_MOTION_TYPE,
                RED_PROP_ROT_DIR,
                RED_START_LOC,
                RED_END_LOC,
                RED_START_ORI,
                RED_TURNS,
            ]
        ]

        return pictograph_dict
