from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..beat_view import BeatView
    from .beat_deleter import BeatDeleter


class OtherBeatDeleter:
    def __init__(self, deleter: "BeatDeleter"):
        self.deleter = deleter

    def delete_non_first_beat(self, selected_beat: "BeatView"):
        self.deleter._delete_beat_and_following(selected_beat)
        last_filled_beat = self.deleter.beat_frame.get.last_filled_beat()
        self.deleter.selection_overlay.select_beat(
            last_filled_beat, toggle_graph_editor=False
        )
        self.deleter.sequence_widget.main_widget.construct_tab.last_beat = (
            last_filled_beat.beat
        )
        self.deleter._post_deletion_updates()
