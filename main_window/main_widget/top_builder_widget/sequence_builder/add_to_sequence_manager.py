from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from main_window.main_widget.top_builder_widget.sequence_builder.sequence_builder import (
        SequenceBuilder,
    )
    from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.beat import (
        Beat,
    )


class AddToSequenceManager:
    def __init__(self, sequence_builder: "SequenceBuilder") -> None:
        self.sequence_builder = sequence_builder

    def create_new_beat(self, clicked_option: "BasePictograph") -> "Beat":
        from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.beat import (
            Beat,
        )

        new_beat = Beat(
            clicked_option.main_widget.top_builder_widget.sequence_widget.beat_frame
        )
        new_beat.setSceneRect(clicked_option.sceneRect())
        pictograph_dict = clicked_option.get.pictograph_dict()
        new_beat.updater.update_pictograph(pictograph_dict)
        self.sequence_builder.last_beat = new_beat
        SW_beat_frame = (
            self.sequence_builder.main_widget.top_builder_widget.sequence_widget.beat_frame
        )
        if not SW_beat_frame.sequence_changed:
            SW_beat_frame.sequence_changed = True
        return new_beat
