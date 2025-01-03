from typing import TYPE_CHECKING

from main_window.main_widget.sequence_widget.beat_frame.beat_view import BeatView

if TYPE_CHECKING:
    from .beat_deleter import BeatDeleter


class FirstBeatDeleter:
    def __init__(self, deleter: "BeatDeleter"):
        self.deleter = deleter

    def delete_first_beat(self, selected_beat: BeatView):
        self.option_picker = self.deleter.main_widget.construct_tab.option_picker
        widgets = self.deleter.widget_collector.collect_widgets()
        views = [option.view for option in self.option_picker.option_pool]
        widgets.extend(views)
        widgets.remove(self.deleter.beat_frame.start_pos_view)
        
        self.deleter.main_widget.fade_manager.widget_fader.fade_and_update(
            widgets,
            callback=lambda: (
                self._delete_beat_and_following(selected_beat),
                self.deleter.selection_overlay.select_beat(
                    self.deleter.beat_frame.start_pos_view, toggle_graph_editor=False
                ),
            ),
            duration=300,
        )

    def _delete_beat_and_following(self, start_beat: BeatView):
        self.deleter.sequence_widget.main_widget.construct_tab.last_beat = (
            self.deleter.beat_frame.start_pos_view.beat
        )
        self.deleter.beat_frame.selection_overlay.deselect_beat()
        beats = self.deleter.beat_frame.beats
        start_index = beats.index(start_beat)
        for beat in beats[start_index:]:
            self.deleter._delete_beat(beat)
        self.deleter._post_deletion_updates()

        self.option_picker = self.deleter.main_widget.construct_tab.option_picker
        self.option_picker._update_pictographs()
