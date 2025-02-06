from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtCore import Qt


from base_widgets.base_beat_frame import BaseBeatFrame
from main_window.main_widget.browse_tab.temp_beat_frame.temp_beat_frame_layout_manager import (
    TempBeatFrameLayoutManager,
)

from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.sequence_widget.beat_frame.beat import Beat
from main_window.main_widget.sequence_widget.beat_frame.beat_view import BeatView
from main_window.main_widget.sequence_widget.beat_frame.image_export_manager.image_export_manager import (
    ImageExportManager,
)
from main_window.main_widget.sequence_widget.beat_frame.start_pos_beat import (
    StartPositionBeat,
)
from main_window.main_widget.sequence_widget.beat_frame.start_pos_beat_view import (
    StartPositionBeatView,
)


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import (
        BrowseTab,
    )


class TempBeatFrame(BaseBeatFrame):
    """The purpose of this class is to create images for use within the dictionary or the sequence card tab.
    This beat frame is never seen by the user."""

    def __init__(self, browse_tab: "BrowseTab") -> None:
        super().__init__(browse_tab.main_widget)
        self.main_widget = browse_tab.main_widget
        self.json_manager = self.main_widget.json_manager
        self.browse_tab = browse_tab
        self.settings_manager = self.main_widget.main_window.settings_manager

        self.initialized = True
        self.sequence_changed = False
        self.setObjectName("beat_frame")
        self.setStyleSheet("QFrame#beat_frame { background: transparent; }")
        self._init_beats()
        self._setup_components()
        self._setup_layout()

    def _init_beats(self):
        self.beat_views = [BeatView(self, number=i + 1) for i in range(64)]
        for beat in self.beat_views:
            beat.hide()

    def _setup_components(self) -> None:
        self.layout_manager = TempBeatFrameLayoutManager(self)
        self.start_pos_view = StartPositionBeatView(self)
        self.start_pos = StartPositionBeat(self)
        self.export_manager = ImageExportManager(self, TempBeatFrame)

    def _setup_layout(self) -> None:
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.start_pos_view, 0, 0)
        for i, beat in enumerate(self.beat_views):
            row, col = divmod(i, 8)
            self.layout.addWidget(beat, row + 1, col + 1)
        self.layout_manager.configure_beat_frame(16)

    def add_beat_to_sequence(self, new_beat: "BasePictograph") -> None:
        next_beat_index = self.get.next_available_beat()

        if (
            next_beat_index is not None
            and self.beat_views[next_beat_index].is_filled is False
        ):
            self.beat_views[next_beat_index].set_beat(new_beat, next_beat_index + 1)
            self.json_manager.updater.update_current_sequence_file_with_beat(
                self.beat_views[next_beat_index].beat
            )
            self.update_current_word()
            self.adjust_layout_to_sequence_length()

    def adjust_layout_to_sequence_length(self):
        last_filled_index = self.get.next_available_beat() or len(self.beat_views)
        self.layout_manager.configure_beat_frame(last_filled_index)

    def get_last_filled_beat(self) -> BeatView:
        for beat_view in reversed(self.beat_views):
            if beat_view.is_filled:
                return beat_view
        return self.start_pos_view

    def on_beat_adjusted(self) -> None:
        current_sequence_json = (
            self.json_manager.loader_saver.load_current_sequence_json()
        )
        self.propogate_turn_adjustment(current_sequence_json)

    def propogate_turn_adjustment(self, current_sequence_json) -> None:
        for i, entry in enumerate(current_sequence_json):
            if i == 0:
                continue
            elif i == 1:
                self.update_start_pos_from_current_sequence_json(entry)
            elif i > 1:
                beat = self.beat_views[i - 2].beat
                if beat:
                    if beat.pictograph_dict != entry:
                        beat.updater.update_pictograph(entry)
                        # QApplication.processEvents()

    def update_start_pos_from_current_sequence_json(self, entry: dict) -> None:
        entry["red_attributes"]["start_ori"] = entry["red_attributes"]["end_ori"]
        entry["blue_attributes"]["start_ori"] = entry["blue_attributes"]["end_ori"]
        entry["start_pos"] = entry["end_pos"]
        self.start_pos_view.start_pos.updater.update_pictograph(entry)

    def populate_beat_frame_from_json(
        self, current_sequence_json: list[dict[str, str]]
    ) -> None:

        self.construct_tab = self.main_widget.construct_tab
        if not current_sequence_json:
            return
        self.clear_sequence(
            show_indicator=False, should_reset_to_start_pos_picker=False
        )

        start_pos_beat = self.construct_tab.start_pos_picker.convert_current_sequence_json_entry_to_start_pos_pictograph(
            current_sequence_json
        )
        self.json_manager.start_pos_handler.set_start_position_data(start_pos_beat)
        self.start_pos_view.set_start_pos(start_pos_beat)
        for pictograph_dict in current_sequence_json[1:]:
            if pictograph_dict.get("sequence_start_position"):
                continue
            self.populate_sequence(pictograph_dict)

        last_beat = self.get_last_filled_beat().beat
        self.construct_tab.last_beat = last_beat

        if self.construct_tab.start_pos_picker.isVisible():
            self.construct_tab.transition_to_option_picker()

    def populate_sequence(self, pictograph_dict: dict) -> None:
        pictograph = Beat(self)
        pictograph.updater.update_pictograph(pictograph_dict)
        self.add_beat_to_sequence(pictograph)
        self.update_current_word()

    def update_current_word(self):
        self.current_word = self.get.current_word()

    def clear_sequence(
        self, show_indicator=True, should_reset_to_start_pos_picker=True
    ) -> None:
        self._reset_beat_frame()

        if should_reset_to_start_pos_picker:
            self.construct_tab.transition_to_start_pos_picker()
        self.construct_tab.last_beat = self.start_pos
        self.json_manager.loader_saver.clear_current_sequence_file()

        # Reset the layout to the smallest possible amount
        if self.settings_manager.global_settings.get_grow_sequence():
            self.layout_manager.configure_beat_frame(0)

    def _reset_beat_frame(self) -> None:
        for beat_view in self.beat_views:
            beat_view.setScene(beat_view.blank_beat)
            beat_view.is_filled = False
        self.start_pos_view.setScene(self.start_pos_view.blank_beat)
        self.start_pos_view.is_filled = False
