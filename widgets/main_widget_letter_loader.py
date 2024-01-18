from typing import TYPE_CHECKING, Dict, List, Optional
from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QTabWidget,
)
from utilities.TypeChecking.letter_lists import all_letters
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QResizeEvent
import pandas as pd
from constants import (
    BLUE_END_LOC,
    BLUE_MOTION_TYPE,
    BLUE_PROP_ROT_DIR,
    BLUE_START_LOC,
    BLUE_START_ORI,
    BLUE_TURNS,
    DIAMOND,
    END_POS,
    IN,
    LETTER,
    RED_END_LOC,
    RED_MOTION_TYPE,
    RED_PROP_ROT_DIR,
    RED_START_LOC,
    RED_START_ORI,
    RED_TURNS,
    STAFF,
    START_POS,
)
from utilities.TypeChecking.TypeChecking import Letters
from widgets.image_cache_manager import ImageCacheManager
from widgets.main_tab_widget import MainTabWidget
from widgets.main_widget_layout_manager import MainWidgetLayoutManager
from .ig_tab.ig_tab import IGTab
from .option_picker_tab.option_picker_tab import OptionPickerTab
from .graph_editor_tab.graph_editor_tab import GraphEditorTab
from .graph_editor_tab.graph_editor_key_event_handler import KeyEventHandler
from objects.pictograph.pictograph import Pictograph
from .sequence_widget.sequence_widget import SequenceWidget

if TYPE_CHECKING:
    from main import MainWindow
    from widgets.main_widget import MainWidget


class MainWidgetLetterLoader:
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
