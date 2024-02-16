from typing import TYPE_CHECKING
import pandas as pd
from Enums.Enums import Letters
from constants import *

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class LetterLoader:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget

    def load_all_letters(self) -> dict[Letters, list[dict]]:
        df = pd.read_csv("PictographDataframe.csv")
        df = df.sort_values(by=[LETTER, START_POS, END_POS])
        df = self.add_turns_and_ori_to_pictograph_dict(df)
        letters = {
            self.get_letter_enum_by_value(letter_str): df[
                df[LETTER] == letter_str
            ].to_dict(orient="records")
            for letter_str in df[LETTER].unique()
        }
        return letters

    def add_turns_and_ori_to_pictograph_dict(self, pictograph_dict) -> pd.DataFrame:
        pictograph_dict[BLUE_TURNS] = 0
        pictograph_dict[RED_TURNS] = 0
        pictograph_dict[BLUE_START_ORI] = IN
        pictograph_dict[RED_START_ORI] = IN
        return pictograph_dict

    @staticmethod
    def get_letter_enum_by_value(letter_value: str) -> Letters:
        for letter in Letters.__members__.values():
            if letter.value == letter_value:
                return letter
        raise ValueError(f"No matching Letters enum for value: {letter_value}")
