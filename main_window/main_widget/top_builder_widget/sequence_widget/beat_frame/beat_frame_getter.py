from typing import TYPE_CHECKING

from utilities.word_simplifier import WordSimplifier


if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.beat import (
        BeatView,
    )
    from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )


class BeatFrameGetter:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        self.beat_frame = beat_frame

    def next_available_beat(self) -> int:
        current_beat = 0
        for beat_view in self.beat_frame.beats:
            if beat_view.is_filled:
                current_beat += beat_view.beat.duration
            else:
                return current_beat
        return current_beat

    def last_filled_beat(self) -> "BeatView":
        for beat_view in reversed(self.beat_frame.beats):
            if beat_view.is_filled:
                return beat_view
        return self.beat_frame.start_pos_view

    def current_word(self) -> str:
        word = ""
        for beat_view in self.beat_frame.beats:
            if beat_view.is_filled:
                word += beat_view.beat.letter.value
        return WordSimplifier.simplify_repeated_word(word)

    def index_of_currently_selected_beat(self) -> int:
        for i, beat in enumerate(self.beat_frame.beats):
            if beat.is_selected:
                return i
        return 0