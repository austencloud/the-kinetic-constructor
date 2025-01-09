from typing import TYPE_CHECKING
from main_window.main_widget.sequence_widget.beat_frame.beat_view import BeatView
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .layout_preview_beat_frame import LayoutPreviewBeatFrame


class LayoutPreviewBeatView(BeatView):
    """A beat view designed for the layout preview frame."""

    def __init__(self, beat_frame: "LayoutPreviewBeatFrame", number: int) -> None:
        self.beat_frame = beat_frame
        super().__init__(beat_frame, number)
        self.setCursor(Qt.CursorShape.ArrowCursor)

    # def resizeEvent(self, event):
    #     """Override resize to handle dynamic sizing."""
    #     pass
