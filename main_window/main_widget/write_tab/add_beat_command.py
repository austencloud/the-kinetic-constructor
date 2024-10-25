# commands.py
from typing import TYPE_CHECKING
from PyQt6.QtGui import QUndoCommand

if TYPE_CHECKING:
    from .timeline_beat_container import TimelineBeatContainer
    from main_window.main_widget.sequence_widget.beat_frame.beat_view import Beat


class AddBeatCommand(QUndoCommand):
    def __init__(
        self,
        beat_widget: "TimelineBeatContainer",
        beat: "Beat",
        description: str = "Add Beat",
    ):
        super().__init__(description)
        self.beat_widget = beat_widget
        self.beat = beat

    def undo(self):
        self.beat_widget.remove_pictograph()

    def redo(self):
        self.beat_widget.set_pictograph(self.beat)
