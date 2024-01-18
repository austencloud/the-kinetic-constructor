import os
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtWidgets import (
    QSizePolicy,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QTabWidget,
)
from utilities.TypeChecking.letter_lists import all_letters
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QResizeEvent, QWheelEvent, QPixmap
import pandas as pd
from constants import (
    BLUE,
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
    RED,
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
from .ig_tab.ig_tab import IGTab
from .option_picker_tab.option_picker_tab import OptionPickerTab
from .graph_editor_tab.graph_editor_tab import GraphEditorTab
from .graph_editor_tab.graph_editor_key_event_handler import KeyEventHandler
from objects.pictograph.pictograph import Pictograph
from PyQt6.QtWidgets import QProgressBar
from .sequence_widget.sequence_widget import SequenceWidget
from .styled_splitter import StyledSplitter

if TYPE_CHECKING:
    from main import MainWindow
    from widgets.main_widget import MainWidget
from typing import Generator
import os


class ImageCacheManager:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.image_cache = {}
        self.main_widget = main_widget

    def cache_image(self, image_path, pixmap):
        self.image_cache[image_path] = pixmap

    def get_cached_pixmap(self, image_path: str) -> QPixmap | None:
        if image_path not in self.image_cache:
            return None
        if self.image_cache[image_path] is None:
            self.image_cache[image_path] = QPixmap(image_path)
        return self.image_cache[image_path]

    def on_image_generated(self, image_path) -> None:
        print(f"Image generated at {image_path}")
        pixmap = QPixmap(image_path)
        self.cache_image(image_path, pixmap)

    def generate_image_path(self, pictograph: Pictograph) -> str:
        pictograph_dict = pictograph.pictograph_dict
        prop_type = self.main_widget.prop_type
        letter = pictograph_dict[LETTER]
        blue_turns = pictograph.motions[BLUE].turns
        red_turns = pictograph.motions[RED].turns
        blue_turns = pictograph.motions[BLUE].turns
        red_turns = pictograph.motions[RED].turns
        start_to_end_string = f"{pictograph.start_pos}→{pictograph.end_pos}"

        simple_turns_string = f"{blue_turns},{red_turns}"
        image_dir = os.path.join(
            "resources",
            "images",
            "pictographs",
            prop_type,
            simple_turns_string,
            letter,
            start_to_end_string,
        ).replace("\\", "/")

        image_name = (
            f"{letter}_"
            f"({pictograph_dict[START_POS]}→{pictograph_dict[END_POS]})_"
            f"({pictograph_dict[BLUE_MOTION_TYPE]}_"
            f"{pictograph_dict[BLUE_START_LOC]}→{pictograph_dict[BLUE_END_LOC]}_"
            f"{blue_turns}_"
            f"{pictograph.motions[BLUE].start_ori}→{pictograph.motions[BLUE].end_ori})_"
            f"({pictograph_dict[RED_MOTION_TYPE]}_"
            f"{pictograph_dict[RED_START_LOC]}→{pictograph_dict[RED_END_LOC]}_"
            f"{red_turns}_"
            f"{pictograph.motions[RED].start_ori}→{pictograph.motions[RED].end_ori})_"
            f"{prop_type}.png"
        )
        return os.path.join(image_dir, image_name)

    def load_pixmap(self, file_path) -> QPixmap:
        return QPixmap(file_path)

    def get_image_file_paths_for_prop_type(
        self, prop_type
    ) -> Generator[str, Any, None]:
        image_root_dir = os.path.join("resources", "images", "pictographs", prop_type)
        for subdir, _, files in os.walk(image_root_dir):
            for file in files:
                if file.lower().endswith(".png"):
                    yield os.path.join(subdir, file).replace("\\", "/")

    def on_image_generated(self, image_path) -> None:
        print(f"Image generated at {image_path}")
        pixmap = QPixmap(image_path)
        self.cache_image(image_path, pixmap)
