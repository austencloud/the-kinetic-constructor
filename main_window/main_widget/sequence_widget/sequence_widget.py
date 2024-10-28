from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QPoint
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy


from data.constants import FLOAT

from main_window.main_widget.sequence_widget.beat_frame.beat import Beat
from main_window.main_widget.sequence_widget.graph_editor.graph_editor_toggle_tab import (
    GraphEditorToggleTab,
)
from main_window.main_widget.sequence_widget.sequence_clearer import SequenceClearer

from .beat_frame.beat_view import BeatView
from .sequence_auto_completer.sequence_auto_completer import SequenceAutoCompleter
from .beat_frame.sequence_widget_beat_frame import SequenceWidgetBeatFrame
from .add_to_dictionary_manager.add_to_dictionary_manager import AddToDictionaryManager
from .labels.current_word_label import CurrentWordLabel
from .labels.difficulty_label import DifficultyLabel
from .graph_editor.graph_editor import GraphEditor
from .beat_frame.layout_options_dialog import LayoutOptionsDialog
from .labels.sequence_widget_indicator_label import SequenceWidgetIndicatorLabel
from .sequence_widget_pictograph_factory import SequenceWidgetPictographFactory
from .sequence_widget_button_panel import SequenceWidgetButtonPanel
from .sequence_widget_scroll_area import SequenceWidgetScrollArea

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget

class SequenceWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.json_manager = self.main_widget.json_manager
        self.default_beat_quantity = 16

        # Load visibility state of the GraphEditor
        self.is_graph_editor_visible = self.settings_manager.settings.value(
            "graph_editor_visible", True, type=bool
        )

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
        self.button_panel = SequenceWidgetButtonPanel(self)
        self.graph_editor = GraphEditor(self)
        self.pictograph_factory = SequenceWidgetPictographFactory(self)
        self.scroll_area.setWidget(self.beat_frame)

        # Initialize toggle tab and connect it
        self.toggle_tab = GraphEditorToggleTab(self)
        self.toggle_tab.toggled.connect(self.toggle_graph_editor)

        # Animation for expanding/collapsing the GraphEditor and toggle tab
        self.graph_editor_animation = QPropertyAnimation(self.graph_editor, b"maximumHeight")
        self.graph_editor_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.graph_editor_animation.setDuration(300)  # 300ms for smooth animation

        # Animation for the toggle tab to move with the GraphEditor
        self.toggle_tab_animation = QPropertyAnimation(self.toggle_tab, b"pos")
        self.toggle_tab_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.toggle_tab_animation.setDuration(300)

        # Group both animations for simultaneous execution
        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(self.graph_editor_animation)
        self.animation_group.addAnimation(self.toggle_tab_animation)

    def _setup_labels(self):
        self.indicator_label = SequenceWidgetIndicatorLabel(self)
        self.current_word_label = CurrentWordLabel(self)
        self.difficulty_label = DifficultyLabel(self)

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)

        self.current_word_layout = QVBoxLayout()
        self.current_word_layout.addWidget(self.current_word_label)
        self.current_word_layout.addWidget(self.difficulty_label)

        # Place components with toggle tab above the GraphEditor
        self.layout.addLayout(self.current_word_layout, 1)
        self.layout.addLayout(self.beat_frame_layout, 12)
        self.layout.addWidget(self.indicator_label, 1)
        self.layout.addWidget(self.toggle_tab, alignment=Qt.AlignmentFlag.AlignBottom)
        self.layout.addWidget(self.graph_editor, 5)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set the visibility state on load
        self.update_graph_editor_visibility()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setLayout(self.layout)


    def toggle_graph_editor(self):
        """Animate the opening or closing of the GraphEditor and toggle tab."""
        editor_height = self.main_widget.height() // 4  # Full height for the GraphEditor

        if self.is_graph_editor_visible:
            # Collapse to zero height
            self.graph_editor_animation.setStartValue(self.graph_editor.height())
            self.graph_editor_animation.setEndValue(0)
            
            # Move toggle to bottom
            toggle_bottom_position = QPoint(
                self.toggle_tab.pos().x(),
                self.height() - self.toggle_tab.height()  # Ensure it stays visible at the bottom
            )
            self.toggle_tab_animation.setStartValue(self.toggle_tab.pos())
            self.toggle_tab_animation.setEndValue(toggle_bottom_position)
            self.is_graph_editor_visible = False
        else:
            # Expand graph editor to full height
            self.graph_editor_animation.setStartValue(0)
            self.graph_editor_animation.setEndValue(editor_height)

            # Reset toggle tab to above GraphEditor
            toggle_top_position = self.graph_editor.pos() - QPoint(0, self.toggle_tab.height())
            self.toggle_tab_animation.setStartValue(self.toggle_tab.pos())
            self.toggle_tab_animation.setEndValue(toggle_top_position)
            self.is_graph_editor_visible = True

        self.animation_group.start()
        self.save_graph_editor_state()

    def update_graph_editor_visibility(self):
        """Set the initial state of the GraphEditor based on saved settings."""
        if self.is_graph_editor_visible:
            self.graph_editor.setMaximumHeight(self.main_widget.height() // 4)
        else:
            self.graph_editor.setMaximumHeight(0)
            self.toggle_tab.move(
                self.toggle_tab.pos().x(), self.height() - self.toggle_tab.height()
            )

    def save_graph_editor_state(self):
        """Save the visibility state of the GraphEditor."""
        self.settings_manager.settings.setValue(
            "graph_editor_visible", self.is_graph_editor_visible
        )

    def update_current_word_from_beats(self):
        current_word = self.beat_frame.get.current_word()
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
        self.update_current_word_from_beats()

    def _setup_beat_frame_layout(self):
        self.beat_frame_layout = QHBoxLayout()
        self.beat_frame_layout.addWidget(self.scroll_area, 10)
        self.beat_frame_layout.addWidget(self.button_panel, 1)
        self.beat_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.beat_frame_layout.setSpacing(0)

    def showEvent(self, event):
        super().showEvent(event)
        # QTimer.singleShot(0, self.post_show_initialization)

    def post_show_initialization(self):
        self.update_current_word_from_beats()

    def _setup_indicator_label_layout(self):
        self.indicator_label_layout = QHBoxLayout()
        self.indicator_label_layout.addStretch(1)
        self.indicator_label_layout.addWidget(self.indicator_label)
        self.indicator_label_layout.addStretch(1)

    def create_new_beat_and_add_to_sequence(
        self,
        pictograph_dict: dict,
        override_grow_sequence=False,
        update_word=True,
        update_level=True,
        reversal_info=None,
    ) -> None:
        new_beat = Beat(self.beat_frame, duration=pictograph_dict.get("duration", 1))
        new_beat.updater.update_pictograph(pictograph_dict)
        if reversal_info:
            new_beat.blue_reversal = reversal_info.get("blue_reversal", False)
            new_beat.red_reversal = reversal_info.get("red_reversal", False)
        self.beat_frame.beat_adder.add_beat_to_sequence(
            new_beat,
            override_grow_sequence=override_grow_sequence,
            update_word=update_word,
            update_level=update_level,
        )
        for motion in new_beat.motions.values():
            if motion.motion_type == FLOAT:
                letter = self.main_widget.letter_determiner.determine_letter(motion)
                new_beat.letter = letter
                new_beat.tka_glyph.update_tka_glyph()
        self.main_widget.sequence_properties_manager.update_sequence_properties()

    def resize_sequence_widget(self) -> None:
        # self.setMinimumWidth(floor(self.main_widget.width() * 0.5))
        self.current_word_label.resize_current_word_label()
        self.button_panel.resize_button_frame()
        self.beat_frame.resize_beat_frame()
        self.graph_editor.resize_graph_editor()

    def resizeEvent(self, event):
        self.resize_sequence_widget()
        super().resizeEvent(event)
