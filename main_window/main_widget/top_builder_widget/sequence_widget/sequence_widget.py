from typing import TYPE_CHECKING
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout


from main_window.main_widget.top_builder_widget.sequence_widget.sequence_clearer import (
    SequenceClearer,
)

from .beat_frame.beat import Beat, BeatView
from .sequence_auto_completer.sequence_auto_completer import SequenceAutoCompleter
from .beat_frame.sequence_widget_beat_frame import SequenceWidgetBeatFrame
from .add_to_dictionary_manager.add_to_dictionary_manager import AddToDictionaryManager
from .labels.current_word_label import CurrentWordLabel
from .labels.difficulty_label import DifficultyLabel
from .graph_editor.graph_editor import GraphEditor
from .beat_frame.layout_options_dialog import LayoutOptionsDialog
from .labels.sequence_widget_indicator_label import SequenceWidgetIndicatorLabel
from .sequence_widget_pictograph_factory import SequenceWidgetPictographFactory
from .sequence_widget_button_frame import SequenceWidgetButtonFrame
from .sequence_widget_scroll_area import SequenceWidgetScrollArea

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.top_builder_widget import (
        TopBuilderWidget,
    )


class SequenceWidget(QWidget):
    def __init__(self, top_builder_widget: "TopBuilderWidget") -> None:
        super().__init__()
        self.top_builder_widget = top_builder_widget
        self.main_widget = top_builder_widget.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.json_manager = self.main_widget.json_manager

        self.default_beat_quantity = 16

        self._setup_components()
        self._setup_cache()
        self._setup_beat_frame_layout()
        self._setup_indicator_label_layout()
        self._setup_layout()

    def _setup_components(self):
        self._setup_labels()
        self.scroll_area = SequenceWidgetScrollArea(self)
        self.beat_frame = SequenceWidgetBeatFrame(self)
        self.add_to_dictionary_manager = AddToDictionaryManager(self)
        self.autocompleter = SequenceAutoCompleter(self)
        self.sequence_clearer = SequenceClearer(self)
        self.button_frame = SequenceWidgetButtonFrame(self)
        self.graph_editor = GraphEditor(self)
        self.pictograph_factory = SequenceWidgetPictographFactory(self)
        self.scroll_area.setWidget(self.beat_frame)

    def _setup_labels(self):
        self.indicator_label = SequenceWidgetIndicatorLabel(self)
        self.current_word_label = CurrentWordLabel(self)
        self.difficulty_label = DifficultyLabel(self)

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)

        self.current_word_layout = QVBoxLayout()
        self.current_word_layout.addWidget(self.current_word_label)
        self.current_word_layout.addWidget(self.difficulty_label)

        self.layout.addLayout(self.current_word_layout, 1)
        self.layout.addLayout(self.beat_frame_layout, 12)
        self.layout.addWidget(self.indicator_label, 1)
        self.layout.addWidget(self.graph_editor, 4)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

    def update_current_word(self):
        current_word = self.beat_frame.get_current_word()
        self.current_word_label.set_current_word(current_word)

    def update_difficulty_label(self):
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        difficulty_level = (
            self.main_widget.sequence_level_evaluator.get_sequence_difficulty_level(
                sequence
            )
        )
        self.difficulty_label.set_difficulty_level(difficulty_level)

    def _setup_cache(self):
        self.SW_pictograph_cache: dict[str, Beat] = {}

    def show_options_panel(self):
        self.options_panel = LayoutOptionsDialog(self)
        self.options_panel.exec()

    def _get_current_beat_frame_state(self) -> dict:
        num_beats = sum(1 for beat in self.beat_frame.beats if beat.isVisible())
        grow_sequence = self.settings_manager.global_settings.get_grow_sequence()
        rows, cols = self._calculate_current_layout()

        return {
            "num_beats": num_beats,
            "rows": rows,
            "cols": cols,
            "grow_sequence": grow_sequence,
        }

    def _calculate_current_layout(self) -> tuple:
        layout = self.beat_frame.layout

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
        self.beat_frame_layout.addWidget(self.scroll_area, 10)
        self.beat_frame_layout.addWidget(self.button_frame, 1)
        self.beat_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.beat_frame_layout.setSpacing(0)

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self.post_show_initialization)

    def post_show_initialization(self):
        self.update_current_word()

    def _setup_indicator_label_layout(self):
        self.indicator_label_layout = QHBoxLayout()
        self.indicator_label_layout.addStretch(1)
        self.indicator_label_layout.addWidget(self.indicator_label)
        self.indicator_label_layout.addStretch(1)

    def create_new_beat_and_add_to_sequence(
        self, pictograph_dict: dict, override_grow_sequence=False, update_word=True
    ) -> None:
        new_beat = Beat(self.beat_frame)
        new_beat.updater.update_pictograph(pictograph_dict)
        self.beat_frame.add_beat_to_sequence(
            new_beat, override_grow_sequence, update_word
        )
        self.json_manager.updater.update_sequence_properties()  # Recalculate properties after each update

    def resize_sequence_widget(self) -> None:
        self.current_word_label.resize_current_word_label()
        self.button_frame.resize_button_frame()
        self.graph_editor.resize_graph_editor()
        self.beat_frame.resize_beat_frame()
