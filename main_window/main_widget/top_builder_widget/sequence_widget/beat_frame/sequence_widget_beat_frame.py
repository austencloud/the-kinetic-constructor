from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGridLayout, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent

from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.beat_frame_layout_manager import (
    BeatFrameLayoutManager,
)
from base_widgets.base_beat_frame import BaseBeatFrame

from .beat_deletion_manager import BeatDeletionManager
from .image_export_manager.image_export_manager import ImageExportManager
from .beat_selection_overlay import BeatSelectionOverlay
from .start_pos_beat import StartPositionBeat
from .start_pos_beat import StartPositionBeatView

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )

from .beat import BeatView


class SequenceWidgetBeatFrame(BaseBeatFrame):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget.main_widget)
        self.main_widget = sequence_widget.main_widget
        self.json_manager = self.main_widget.json_manager
        self.sequence_widget = sequence_widget
        self.top_builder_widget = sequence_widget.top_builder_widget
        self.settings_manager = self.main_widget.main_window.settings_manager

        self.initialized = True
        self.sequence_changed = False
        self.setObjectName("beat_frame")
        self.setStyleSheet("QFrame#beat_frame { background: transparent; }")
        self._init_beats()
        self._setup_components()
        self._setup_layout()

    def _init_beats(self):
        self.beats = [BeatView(self, number=i + 1) for i in range(64)]
        for beat in self.beats:
            beat.hide()

    def _setup_components(self) -> None:
        self._setup_start_position_beat()
        self.selection_overlay = BeatSelectionOverlay(self)
        self.layout_manager = BeatFrameLayoutManager(self)
        self.beat_deletion_manager = BeatDeletionManager(self)
        self.image_export_manager = ImageExportManager(self, SequenceWidgetBeatFrame)

    def _setup_start_position_beat(self):
        self.start_pos_view = StartPositionBeatView(self)
        self.start_pos = StartPositionBeat(self)

    def _setup_layout(self) -> None:
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_pos_view.start_pos.initializer.set_nonradial_points_visibility(False)
        self.layout.addWidget(self.start_pos_view, 0, 0)
        for i, beat in enumerate(self.beats):
            row, col = divmod(i, 8)
            self.layout.addWidget(beat, row + 1, col + 1)
        self.layout_manager.configure_beat_frame(16)

    def keyPressEvent(self, event: "QKeyEvent") -> None:
        if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace:
            self.beat_deletion_manager.delete_selected_beat()
        else:
            super().keyPressEvent(event)

    def delete_selected_beat(self) -> None:
        self.beat_deletion_manager.delete_selected_beat()

    def add_beat_to_sequence(self, new_beat: "BasePictograph") -> None:
        next_beat_index = self.find_next_available_beat()
        if next_beat_index == 0:
            self.sequence_widget.difficulty_label.set_difficulty_level(1)
        grow_sequence = self.settings_manager.global_settings.get_grow_sequence()
        if grow_sequence:
            if (
                next_beat_index is not None
                and self.beats[next_beat_index].is_filled is False
            ):
                self.beats[next_beat_index].set_beat(new_beat, next_beat_index + 1)
                self.json_manager.updater.update_current_sequence_file_with_beat(
                    self.beats[next_beat_index]
                )
                self.sequence_widget.update_current_word()
                self.adjust_layout_to_sequence_length()
                self.sequence_builder = (
                    self.main_widget.top_builder_widget.sequence_builder
                )
                self.sequence_builder.last_beat = self.beats[next_beat_index].beat
                # select the beat with the selection overlay
                # self.selection_overlay.select_beat(new_beat.view)

        elif not grow_sequence:
            if (
                next_beat_index is not None
                and self.beats[next_beat_index].is_filled is False
                and self.beats[next_beat_index].isVisible()
            ):
                self.beats[next_beat_index].set_beat(new_beat, next_beat_index + 1)
                self.json_manager.updater.update_current_sequence_file_with_beat(
                    self.beats[next_beat_index]
                )
                self.sequence_widget.update_current_word()
                self.sequence_builder = (
                    self.main_widget.top_builder_widget.sequence_builder
                )
                self.sequence_builder.last_beat = self.beats[next_beat_index].beat
                # self.selection_overlay.select_beat(new_beat.view)

    def find_next_available_beat(self) -> int:
        for i, beat in enumerate(self.beats):
            if not beat.is_filled:
                return i
        return None

    def adjust_layout_to_sequence_length(self):
        last_filled_index = self.find_next_available_beat() or len(self.beats)
        self.layout_manager.configure_beat_frame(last_filled_index)

    def get_last_filled_beat(self) -> BeatView:
        for beat_view in reversed(self.beats):
            if beat_view.is_filled:
                return beat_view
        return self.start_pos_view

    def on_beat_adjusted(self) -> None:
        current_sequence_json = (
            self.json_manager.loader_saver.load_current_sequence_json()
        )
        self.propogate_turn_adjustment(current_sequence_json)
        if len(current_sequence_json) > 2:
            self.sequence_widget.update_difficulty_label()

    def propogate_turn_adjustment(self, current_sequence_json) -> None:
        for i, entry in enumerate(current_sequence_json):
            if i == 0:
                continue
            elif i == 1:
                self.update_start_pos_from_current_sequence_json(entry)
            elif i > 1:
                beat = self.beats[i - 2].beat
                if beat:
                    if beat.pictograph_dict != entry:
                        beat.updater.update_pictograph(entry)
                        QApplication.processEvents()

    def update_start_pos_from_current_sequence_json(self, entry: dict) -> None:
        entry["red_attributes"]["start_ori"] = entry["red_attributes"]["end_ori"]
        entry["blue_attributes"]["start_ori"] = entry["blue_attributes"]["end_ori"]
        entry["start_pos"] = entry["end_pos"]
        self.start_pos_view.start_pos.updater.update_pictograph(entry)

    def get_index_of_currently_selected_beat(self) -> int:
        for i, beat in enumerate(self.beats):
            if beat.is_selected:
                return i
        return 0

    def resize_beat_frame(self) -> None:
        scrollbar_width = self.sequence_widget.scroll_area.verticalScrollBar().width()
        width = int(
            (
                self.sequence_widget.width()
                - self.sequence_widget.button_frame.width()
                - scrollbar_width
            )
            * 0.8
        )

        height = (
            self.sequence_widget.height()
            - self.sequence_widget.graph_editor.height() * 0.8
        )

        num_cols = max(1, self.layout.columnCount() - 1)
        if num_cols == 0:
            return

        beat_size = min(int(width // (5)), int(height // 6))
        for beat in self.beats:
            beat.setFixedSize(beat_size, beat_size)
        self.start_pos_view.setFixedSize(beat_size, beat_size)
        for beat in self.beats:
            beat.resize_beat_view()
        self.start_pos_view.resize_beat_view()
        QApplication.processEvents()
        self.selection_overlay.update_overlay_position()

    def populate_beat_frame_from_json(
        self, current_sequence_json: list[dict[str, str]]
    ) -> None:
        self.start_pos_manager = (
            self.main_widget.top_builder_widget.sequence_builder.start_pos_picker.start_pos_manager
        )
        self.sequence_builder = self.main_widget.top_builder_widget.sequence_builder
        if not current_sequence_json:
            return
        self.sequence_widget.sequence_clearer.clear_sequence(
            show_indicator=False, should_reset_to_start_pos_picker=False
        )
        start_pos_beat = self.start_pos_manager.convert_current_sequence_json_entry_to_start_pos_pictograph(
            current_sequence_json
        )
        self.json_manager.start_position_handler.set_start_position_data(start_pos_beat)
        self.start_pos_view.set_start_pos(start_pos_beat)
        for pictograph_dict in current_sequence_json[1:]:
            if pictograph_dict.get("sequence_start_position"):
                continue
            self.sequence_widget.create_new_beat_and_add_to_sequence(pictograph_dict)
        self.sequence_widget.update_current_word()
        if len(current_sequence_json) > 2:
            self.sequence_widget.update_difficulty_label()
        else:
            self.sequence_widget.difficulty_label.set_difficulty_level("")
        last_beat = self.sequence_widget.beat_frame.get_last_filled_beat().beat
        self.sequence_builder.last_beat = last_beat

        if self.sequence_builder.start_pos_picker.isVisible():
            self.sequence_builder.transition_to_sequence_building()

        scroll_area = self.sequence_builder.option_picker.scroll_area
        scroll_area.remove_irrelevant_pictographs()
        next_options = (
            self.sequence_builder.option_picker.option_getter.get_next_options(
                current_sequence_json
            )
        )

        scroll_area.add_and_display_relevant_pictographs(next_options)
        self.sequence_builder.option_picker.resize_option_picker()
        self.selection_overlay.select_beat(self.get_last_filled_beat())
