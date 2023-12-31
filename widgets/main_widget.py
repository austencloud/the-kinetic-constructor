from collections import OrderedDict
import os
from typing import TYPE_CHECKING, Any, Optional
from PyQt6.QtCore import QEvent, Qt, QThreadPool
from PyQt6.QtWidgets import (
    QSizePolicy,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QTabWidget,
)
from PyQt6.QtCore import QEvent, Qt, QThreadPool
from PyQt6.QtGui import QWheelEvent, QPixmap
import pandas as pd
from Enums import PictographAttributesDict
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
from widgets.image_generator_tab.ig_tab import IGTab
from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
from widgets.graph_editor_tab.graph_editor_tab import GraphEditorTab
from widgets.graph_editor_tab.key_event_handler import KeyEventHandler
from objects.pictograph.pictograph import Pictograph
from widgets.sequence_widget.sequence_widget import SequenceWidget
from widgets.styled_splitter import StyledSplitter

if TYPE_CHECKING:
    from main import MainWindow
from typing import Generator
import os


class MainWidget(QWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.worker_threads = []  # Add this line to store worker references
        self.image_cache = {}
        self.prop_type = STAFF
        self.grid_mode = DIAMOND
        self.arrows = []
        self.export_handler = None
        self.main_window = main_window
        self.thread_pool = QThreadPool()
        self.image_cache_initialized = False
        self.resize(int(self.main_window.width()), int(self.main_window.height()))
        self.key_event_handler = KeyEventHandler()
        self.letters: PictographAttributesDict = self.load_all_letters()
        self.graph_editor_tab = GraphEditorTab(self)
        self.sequence_widget = SequenceWidget(self)
        self.option_picker_tab = OptionPickerTab(self)
        self.image_generator_tab = IGTab(self)
        self.image_generator_tab.imageGenerated.connect(self.on_image_generated)
        self.configure_layouts()
        self.pixmap_cache = {}

    def load_all_letters(self) -> dict:
        df = pd.read_csv("PictographDataframe.csv")
        df = df.sort_values(by=[LETTER, START_POS, END_POS])

        # Selecting the necessary columns
        df = self.init_dataframe(df)

        # Creating the letters dictionary
        letters = (
            df.groupby(LETTER).apply(lambda x: x.to_dict(orient="records")).to_dict()
        )

        self.letters = letters
        return self.letters

    def init_dataframe(self, df):
        df = df[
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
        df[BLUE_TURNS] = 0
        df[RED_TURNS] = 0
        df[BLUE_START_ORI] = IN
        df[RED_START_ORI] = IN

        df = df[
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

        return df

    def configure_layouts(self) -> None:
        self.horizontal_splitter = StyledSplitter(Qt.Orientation.Horizontal)

        self.left_frame = QFrame()
        self.right_frame = QFrame()

        self.left_layout = QVBoxLayout(self.left_frame)
        self.right_layout = QVBoxLayout(self.right_frame)

        self.left_layout.addWidget(self.sequence_widget)

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(
            """
            QTabWidget::pane { /* The tab widget frame */
                border-top: 2px solid #C2C7CB;
            }


            /* Style the tab using the tab sub-control. Note that
                it uses a QTabBar sub-control called tab. */
            QTabBar::tab {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                            stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                border: 2px solid #C4C4C3;
                border-bottom-color: #C2C7CB; /* same as the pane color */
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 2px;
                font-size: 14px; /* Increase the font size */
            }

            QTabBar::tab:selected, QTabBar::tab:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                            stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
            }

            QTabBar::tab:selected {
                border-color: #9B9B9B;
                border-bottom-color: #C2C7CB; /* same as pane color */
            }

            QTabBar::tab:!selected {
                margin-top: 2px; /* make non-selected tabs look smaller */
            }

            QTabBar::tab:!selected {
                font-size: 14px; /* Increase the font size */
            }

            """
        )
        self.tab_widget.addTab(self.image_generator_tab, "Image Generator")
        self.tab_widget.addTab(self.option_picker_tab, "Option Picker")
        self.tab_widget.addTab(self.graph_editor_tab, "Graph Editor")

        self.left_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.right_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.right_frame.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.right_layout.addWidget(self.tab_widget)

        self.horizontal_splitter.addWidget(self.left_frame)
        self.horizontal_splitter.addWidget(self.right_frame)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(self.horizontal_splitter)
        self.setLayout(self.main_layout)
        # self.initialize_image_cache()

    ### EVENT HANDLERS ###

    def on_splitter_moved(self) -> None:
        self.option_picker_tab.resize_option_picker_tab()
        self.sequence_widget.resize_sequence_widget()

    def eventFilter(self, source, event: QEvent) -> bool:
        if event.type() == QEvent.Type.KeyPress:
            active_pictograph = self.find_active_pictograph()
            if active_pictograph:
                self.key_event_handler.keyPressEvent(event, self, active_pictograph)
                return True

        return super().eventFilter(source, event)

    def deselect_all_except(self, active_pictograph: Pictograph) -> None:
        if self.graph_editor_tab.graph_editor.main_pictograph != active_pictograph:
            self.graph_editor_tab.graph_editor.main_pictograph.clearSelection()

        for beat_view in self.sequence_widget.beat_frame.beats:
            if beat_view.pictograph and beat_view.pictograph != active_pictograph:
                beat_view.pictograph.clearSelection()

    def find_active_pictograph(self) -> Optional[Pictograph]:
        if self.graph_editor_tab.graph_editor.main_pictograph.selectedItems():
            return self.graph_editor_tab.graph_editor.main_pictograph

        for beat_view in self.sequence_widget.beat_frame.beats:
            if beat_view.pictograph and beat_view.pictograph.selectedItems():
                return beat_view.pictograph

        return None

    def wheelEvent(self, event: QWheelEvent | None) -> None:
        return super().wheelEvent(event)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.option_picker_tab.resize_option_picker_tab()
        self.sequence_widget.resize_sequence_widget()

    ### IMAGE CACHE ###

    def on_image_generated(self, image_path) -> None:
        print(f"Image generated at {image_path}")
        pixmap = QPixmap(image_path)
        self.cache_image(image_path, pixmap)

    def get_image_file_paths_for_prop_type(
        self, prop_type
    ) -> Generator[str, Any, None]:
        # Adapt this method to only yield file paths for the current prop_type
        image_root_dir = os.path.join("resources", "images", "pictographs", prop_type)
        for subdir, _, files in os.walk(image_root_dir):
            for file in files:
                if file.lower().endswith(".png"):
                    yield os.path.join(subdir, file).replace("\\", "/")

    def load_pixmap(self, file_path) -> QPixmap:
        # Load the pixmap from the disk
        return QPixmap(file_path)

    def cache_image(self, image_path, pixmap):
        # This will be executed in the main thread because of the signal-slot mechanism
        self.image_cache[image_path] = pixmap

    def get_cached_pixmap(self, image_path: str) -> QPixmap | None:
        if image_path not in self.image_cache:
            return None
        if self.image_cache[image_path] is None:
            self.image_cache[image_path] = QPixmap(image_path)
        return self.image_cache[image_path]

    def generate_image_path(self, pictograph: Pictograph) -> str:
        pictograph_dict = pictograph.pictograph_dict
        prop_type = self.prop_type
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
            f"{pictograph.motions[BLUE].start_or}→{pictograph.motions[BLUE].end_ori})_"
            f"({pictograph_dict[RED_MOTION_TYPE]}_"
            f"{pictograph_dict[RED_START_LOC]}→{pictograph_dict[RED_END_LOC]}_"
            f"{red_turns}_"
            f"{pictograph.motions[RED].start_or}→{pictograph.motions[RED].end_ori})_"
            f"{prop_type}.png"
        )
        return os.path.join(image_dir, image_name)
