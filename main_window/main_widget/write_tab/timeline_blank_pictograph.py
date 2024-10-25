# timeline_beat_widget.py
from typing import TYPE_CHECKING
from main_window.main_widget.sequence_widget.beat_frame.beat import Beat

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.timeline_beat_container import (
        TimelineBeatContainer,
    )


class TimelineBlankPictograph(Beat):
    def __init__(self, beat_container: "TimelineBeatContainer") -> None:
        super().__init__(beat_container.main_widget)
        self.is_blank = True
