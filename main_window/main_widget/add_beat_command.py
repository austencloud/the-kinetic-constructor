# commands.py
from typing import TYPE_CHECKING
from PyQt6.QtGui import QUndoCommand
if TYPE_CHECKING:
    from .timeline_beat_widget import TimelineBeatWidget
    from main_window.main_widget.sequence_widget.beat_frame.beat import Beat


class AddBeatCommand(QUndoCommand):
    def __init__(
        self,
        beat_widget: "TimelineBeatWidget",
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
