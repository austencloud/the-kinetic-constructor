from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph

    from main_window.main_widget.top_builder_widget.sequence_builder.manual_builder import (
        ManualBuilderWidget,
    )
    from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.beat import (
        Beat,
    )


class AddToSequenceManager:
    def __init__(self, manual_builder: "ManualBuilderWidget") -> None:
        self.manual_builder = manual_builder

    def create_new_beat(self, clicked_option: "BasePictograph") -> "Beat":
        from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.beat import (
            Beat,
        )

        new_beat = Beat(clicked_option.main_widget.sequence_widget.beat_frame)
        new_beat.setSceneRect(clicked_option.sceneRect())
        pictograph_dict = clicked_option.get.pictograph_dict()

        pictograph_dict["duration"] = 1
        pictograph_dict = dict(
            list(pictograph_dict.items())[:1]
            + [("duration", 1)]
            + list(pictograph_dict.items())[1:]
        )

        new_beat.updater.update_pictograph(pictograph_dict)
        self.manual_builder.last_beat = new_beat
        SW_beat_frame = self.manual_builder.main_widget.sequence_widget.beat_frame
        if not SW_beat_frame.sequence_changed:
            SW_beat_frame.sequence_changed = True
        return new_beat
