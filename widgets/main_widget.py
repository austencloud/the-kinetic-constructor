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
from .graph_editor_tab.graph_editor_key_event_handler import GraphEditorKeyEventHandler
from objects.pictograph.pictograph import Pictograph
from PyQt6.QtWidgets import QProgressBar
from .sequence_widget.sequence_widget import SequenceWidget
from .styled_splitter import StyledSplitter

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
        self.all_pictographs: Dict[Letters, Dict[str, Pictograph]] = {
            letter: {} for letter in all_letters
        }
        self.export_handler = None
        self.main_window = main_window
        self.image_cache_initialized = False
        self.resize(int(self.main_window.width()), int(self.main_window.height()))
        self.key_event_handler = GraphEditorKeyEventHandler()
        self.letters: Dict[Letters, List[Dict]] = self.load_all_letters()
        self.sequence_widget = SequenceWidget(self)
        self.graph_editor_tab = GraphEditorTab(self)
        self.ig_tab = IGTab(self)
        self.option_picker_tab = OptionPickerTab(self)

        self.ig_tab.imageGenerated.connect(self.on_image_generated)
        self.configure_layouts()
        self.pixmap_cache = {}

    def update_pictographs(self, created_pictographs: dict) -> None:
        for key, pictograph in created_pictographs.items():
            self.all_pictographs[key] = pictograph

    def load_all_letters(self) -> dict:
        df: pd.Series = pd.read_csv("PictographDataframe.csv")
        df = df.sort_values(by=[LETTER, START_POS, END_POS])

        # Selecting the necessary columns
        df = self.add_turns_and_ori_to_pictograph_dict(df)

        # Creating the letters dictionary
        letters = (
            df.groupby(LETTER).apply(lambda x: x.to_dict(orient="records")).to_dict()
        )

        self.letters = letters
        return self.letters

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

    def configure_layouts(self) -> None:
        self.horizontal_splitter = StyledSplitter(Qt.Orientation.Horizontal)

        self.left_frame = QFrame()
        self.left_layout = QVBoxLayout(self.left_frame)
        self.left_layout.addWidget(self.sequence_widget)

        self.right_frame = QFrame()
        self.right_layout = QVBoxLayout(self.right_frame)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(
            """
            QTabWidget::pane {
                border: 1px solid black;
                background: white;
            }

            QTabWidget::tab-bar:top {
                top: 1px;
            }

            QTabWidget::tab-bar:bottom {
                bottom: 1px;
            }

            QTabWidget::tab-bar:left {
                right: 1px;
            }

            QTabWidget::tab-bar:right {
                left: 1px;
            }

            QTabBar::tab {
                border: 1px solid black;
            }

            QTabBar::tab:selected {
                background: white;
            }

            QTabBar::tab:!selected {
                background: silver;
            }

            QTabBar::tab:!selected:hover {
                background: #999;
            }

            QTabBar::tab:top:!selected {
                margin-top: 3px;
            }

            QTabBar::tab:bottom:!selected {
                margin-bottom: 3px;
            }

            QTabBar::tab:top, QTabBar::tab:bottom {
                min-width: 8ex;
                margin-right: -1px;
                padding: 5px 10px 5px 10px;
            }

            QTabBar::tab:top:selected {
                border-bottom-color: none;
            }

            QTabBar::tab:bottom:selected {
                border-top-color: none;
            }

            QTabBar::tab:top:last, QTabBar::tab:bottom:last,
            QTabBar::tab:top:only-one, QTabBar::tab:bottom:only-one {
                margin-right: 0;
            }

            QTabBar::tab:left:!selected {
                margin-right: 3px;
            }

            QTabBar::tab:right:!selected {
                margin-left: 3px;
            }

            QTabBar::tab:left, QTabBar::tab:right {
                min-height: 8ex;
                margin-bottom: -1px;
                padding: 10px 5px 10px 5px;
            }

            QTabBar::tab:left:selected {
                border-left-color: none;
            }

            QTabBar::tab:right:selected {
                border-right-color: none;
            }

            QTabBar::tab:left:last, QTabBar::tab:right:last,
            QTabBar::tab:left:only-one, QTabBar::tab:right:only-one {
                margin-bottom: 0;
            }

            """
        )
        self.tab_widget.addTab(self.ig_tab, "Image Generator")
        self.tab_widget.addTab(self.graph_editor_tab, "Graph Editor")
        self.tab_widget.addTab(self.option_picker_tab, "Option Picker")

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

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(0, self.height() - 20, self.width(), 20)
        self.progress_bar.hide()

    def update_progress(self, value: int) -> None:
        self.progress_bar.setValue(value)

    def loading_finished(self) -> None:
        self.progress_bar.hide()

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
        self.sequence_widget.resize_sequence_widget()
        # self.ig_tab.resize_ig_tab()

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
            f"{pictograph.motions[BLUE].start_ori}→{pictograph.motions[BLUE].end_ori})_"
            f"({pictograph_dict[RED_MOTION_TYPE]}_"
            f"{pictograph_dict[RED_START_LOC]}→{pictograph_dict[RED_END_LOC]}_"
            f"{red_turns}_"
            f"{pictograph.motions[RED].start_ori}→{pictograph.motions[RED].end_ori})_"
            f"{prop_type}.png"
        )
        return os.path.join(image_dir, image_name)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.main_window._set_dimensions()

    def display_pictograph(self, pictograph_key):
        if pictograph_key not in self.all_pictographs:
            self.pictograph_factory.get_or_create_pictograph(pictograph_key)
        pictograph = self.all_pictographs[pictograph_key]
