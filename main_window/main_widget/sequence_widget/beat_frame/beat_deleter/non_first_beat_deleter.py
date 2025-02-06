from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..beat_view import BeatView
    from .beat_deleter import BeatDeleter


class NonFirstBeatDeleter:
    def __init__(self, deleter: "BeatDeleter"):
        self.deleter = deleter

    def delete_non_first_beat(self, selected_beat: "BeatView"):
        index_of_selected_beat = self.deleter.beat_frame.beat_views.index(selected_beat)
        self.option_picker = self.deleter.main_widget.construct_tab.option_picker
        widgets = self.deleter.widget_collector.collect_shared_widgets()
        views = [option.view for option in self.option_picker.option_pool]
        widgets.extend(views)
        widgets.remove(self.deleter.beat_frame.start_pos_view)
        beats_to_remove = self.deleter.beat_frame.beat_views[:index_of_selected_beat]
        for beat in beats_to_remove:
            widgets.remove(beat)
        last_filled_beat = self.deleter.beat_frame.get.last_filled_beat()

        self.deleter.sequence_widget.main_widget.construct_tab.last_beat = (
            last_filled_beat.beat
        )

        self.deleter.main_widget.fade_manager.widget_fader.fade_and_update(
            widgets,
            callback=lambda: self._delete_beat_and_following(selected_beat),
            duration=300,
        )

    def _delete_beat_and_following(self, beat: "BeatView"):
        self.deleter.sequence_widget.main_widget.construct_tab.last_beat = (
            self.deleter.beat_frame.start_pos_view.beat
        )
        self.deleter.selection_overlay.deselect_beat()
        beats = self.deleter.beat_frame.beat_views
        index = beats.index(beat)
        for beat in beats[index:]:
            self.deleter._delete_beat(beat)
        self.deleter._post_deletion_updates()

        self.option_picker = self.deleter.main_widget.construct_tab.option_picker
        self.option_picker._update_pictographs()
        if index > 0:
            self.deleter.selection_overlay.select_beat(
                beats[index - 1], toggle_animation=False, defer_show=True
            )
