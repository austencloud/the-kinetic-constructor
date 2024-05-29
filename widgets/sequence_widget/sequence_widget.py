from typing import TYPE_CHECKING
from PyQt6.QtGui import QShowEvent
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QScrollArea
from PyQt6.QtCore import Qt

from sequence_autocompleter.sequence_autocompleter import SequenceAutocompleter
from widgets.sequence_widget.add_to_dictionary_manager import AddToDictionaryManager
from widgets.sequence_widget.current_word_label import CurrentWordLabel

from ..graph_editor.graph_editor import GraphEditor
from .SW_beat_frame.SW_beat_frame import SW_BeatFrame
from .SW_beat_frame.SW_layout_options_dialog import SW_LayoutOptionsDialog
from ..indicator_label import IndicatorLabel
from .SW_pictograph_factory import SW_PictographFactory
from .SW_beat_frame.beat import Beat, BeatView
from .SW_button_frame import SW_ButtonFrame

if TYPE_CHECKING:
    from ..main_widget.top_builder_widget import TopBuilderWidget


class SequenceWidget(QWidget):
    def __init__(self, top_builder_widget: "TopBuilderWidget") -> None:
        super().__init__()
        self.top_builder_widget = top_builder_widget
        self.main_widget = top_builder_widget.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.default_beat_quantity = 16
        self._setup_components()
        self._configure_scroll_area()
        self._setup_cache()
        self._setup_beat_frame_layout()
        self._setup_indicator_label_layout()
        self._setup_layout()
        self.update_current_word()

    def _setup_cache(self):
        self.SW_pictograph_cache: dict[str, Beat] = {}

    def _setup_components(self):
        self.scroll_area = QScrollArea(self)
        self.indicator_label = IndicatorLabel(self)
        self.current_word_label = CurrentWordLabel(self)  # Add the current word label
        self.beat_frame = SW_BeatFrame(self)
        self.add_to_dictionary_manager = AddToDictionaryManager(self)
        self.button_frame = SW_ButtonFrame(self)
        self.graph_editor = GraphEditor(self)
        self.pictograph_factory = SW_PictographFactory(self)
        self.autocompleter = SequenceAutocompleter(self.beat_frame)

    def _configure_scroll_area(self):
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.beat_frame)
        self.scroll_area.setObjectName("sequence_scroll_area")
        self.scroll_area.setStyleSheet("QScrollArea{background: transparent;}")
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

    def show_options_panel(self):
        current_state = self._get_current_beat_frame_state()
        self.options_panel = SW_LayoutOptionsDialog(self, current_state)
        self.options_panel.exec()  # Use exec() to show the dialog modally

    def _get_current_beat_frame_state(self) -> dict:
        layout = self.beat_frame.layout
        num_beats = sum(1 for beat in self.beat_frame.beats if beat.isVisible())
        grow_sequence = self.settings_manager.get_grow_sequence()
        save_layout = False  # Default value, can be set based on your logic

        rows, cols = self._calculate_current_layout()

        return {
            "num_beats": num_beats,
            "rows": rows,
            "cols": cols,
            "grow_sequence": grow_sequence,
            "save_layout": save_layout,
        }

    def _calculate_current_layout(self) -> tuple:
        layout = self.beat_frame.layout
        row_count = layout.rowCount()
        col_count = layout.columnCount() - 1  # Exclude the start position column

        max_row = 0
        max_col = 0

        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item and isinstance(item.widget(), BeatView):
                position = layout.getItemPosition(i)
                max_row = max(max_row, position[0])
                max_col = max(max_col, position[1])

        return max_row + 1, max_col  # Add 1 to max_row to get the count

    def apply_layout_options(self, cols, rows, num_beats):
        self.beat_frame.layout_manager.rearrange_beats(num_beats, cols, rows)
        self.update_current_word()

    def _setup_beat_frame_layout(self):
        self.beat_frame_layout = QHBoxLayout()
        self.beat_frame_layout.addWidget(self.scroll_area)
        self.beat_frame_layout.addWidget(self.button_frame)
        self.beat_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.beat_frame_layout.setSpacing(0)

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.current_word_label, 1)
        self.layout.addLayout(self.beat_frame_layout, 12)
        self.layout.addWidget(self.indicator_label, 1)
        self.layout.addWidget(self.graph_editor, 6)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event):
        self.layout.update()
        super().resizeEvent(event)

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        QTimer.singleShot(0, self.post_show_initialization)

    def post_show_initialization(self):
        self.resize_sequence_widget()

    def _setup_indicator_label_layout(self):
        self.indicator_label_layout = QHBoxLayout()
        self.indicator_label_layout.addStretch(1)
        self.indicator_label_layout.addWidget(self.indicator_label)
        self.indicator_label_layout.addStretch(1)

    def populate_sequence(self, pictograph_dict: dict) -> None:
        pictograph = Beat(self.beat_frame)
        pictograph.updater.update_pictograph(pictograph_dict)
        self.beat_frame.add_beat_to_sequence(pictograph)
        pictograph_key = (
            pictograph.main_widget.pictograph_key_generator.generate_pictograph_key(
                pictograph_dict
            )
        )
        self.SW_pictograph_cache[pictograph_key] = pictograph
        self.update_current_word()

    def update_current_word(self):
        current_word = self.beat_frame.get_current_word()
        self.current_word_label.set_current_word(current_word)

    def resize_sequence_widget(self) -> None:
        self.current_word_label.resize_current_word_label()
        self.beat_frame.resize_beat_frame()
        self.graph_editor.resize_graph_editor()
        self.button_frame.resize_button_frame()
