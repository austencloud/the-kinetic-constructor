from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from typing import TYPE_CHECKING, Any, Optional
from PyQt6.QtCore import QEvent, Qt, QThreadPool, QRunnable, pyqtSlot
from PyQt6.QtWidgets import (
    QSizePolicy,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QTabWidget,
    QApplication,
)
from PyQt6.QtCore import QThread, QEvent, Qt, pyqtSignal, QRunnable, QThreadPool
from PyQt6.QtGui import QWheelEvent, QPixmap
import pandas as pd
from Enums import GridMode, PropType
from constants.string_constants import (
    BLUE,
    BLUE_TURNS,
    DIAMOND,
    LETTER,
    RED,
    RED_TURNS,
    STAFF,
)
from image_loader_worker import ImageLoaderRunnable
from utilities.TypeChecking.TypeChecking import PictographDataframe
from widgets.image_generator_tab.ig_tab import IGTab
from widgets.option_picker_tab.option import Option
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
        self.letters: PictographDataframe = self.load_all_letters()
        self.graph_editor_tab = GraphEditorTab(self)
        self.sequence_widget = SequenceWidget(self)
        self.option_picker_tab = OptionPickerTab(self)
        self.image_generator_tab = IGTab(self)
        self.image_generator_tab.imageGenerated.connect(self.on_image_generated)
        self.configure_layouts()
        self.pixmap_cache = {}

    def load_all_letters(self) -> PictographDataframe:
        df = pd.read_csv("PictographDataframe.csv")
        letters: PictographDataframe = (
            df.groupby("letter").apply(lambda x: x.to_dict(orient="records")).to_dict()
        )
        return letters

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
        self.tab_widget.addTab(self.option_picker_tab, "Option Picker")
        self.tab_widget.addTab(self.image_generator_tab, "Image Generator")
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

    def initialize_image_cache(self) -> None:
        image_paths = list(self.get_image_file_paths_for_prop_type(self.prop_type))
        for image_path in image_paths:
            runnable = ImageLoaderRunnable(image_path)
            runnable.signals.finished.connect(self.cache_image)
            self.thread_pool.start(runnable)
            self.worker_threads.append(runnable)
        self.image_cache_initialized = True
        
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
        pd_row_data = pictograph.pd_row_data
        prop_type = self.prop_type
        letter = pd_row_data[LETTER]
        blue_turns = pictograph.motions[BLUE].turns
        red_turns = pictograph.motions[RED].turns
        blue_motion_type_prefix = pictograph.motions[BLUE].motion_type[0]
        red_motion_type_prefix = pictograph.motions[RED].motion_type[0]
        blue_turns = pictograph.motions[BLUE].turns
        red_turns = pictograph.motions[RED].turns
        start_to_end_string = f"{pictograph.start_position}→{pictograph.end_position}"
        turns_string = (
            f"{blue_motion_type_prefix}{blue_turns},{red_motion_type_prefix}{red_turns}"
        )
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

        blue_end_orientation = pictograph.motions[BLUE].get_end_orientation()
        red_end_orientation = pictograph.motions[RED].get_end_orientation()

        image_name = (
            f"{letter}_"
            f"({pd_row_data.name[0]}→{pd_row_data.name[1]})_"
            f"({pd_row_data["blue_motion_type"]}_{pd_row_data['blue_start_location']}→{pd_row_data['blue_end_location']}_"
            f"{blue_turns}_"
            f"{pd_row_data['blue_start_orientation']}→{blue_end_orientation})_"
            f"({pd_row_data["red_motion_type"]}_{pd_row_data['red_start_location']}→{pd_row_data['red_end_location']}_"
            f"{red_turns}_"
            f"{pd_row_data['red_start_orientation']}→{red_end_orientation})_"
            f"{prop_type}.png"
        )
        return os.path.join(image_dir, image_name)
