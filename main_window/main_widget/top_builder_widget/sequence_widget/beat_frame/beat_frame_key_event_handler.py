from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QWidget  # Import QWidget

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )


class BeatFrameKeyEventHandler(QWidget): 
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        super().__init__(beat_frame)
        self.beat_frame = beat_frame
        self.beat_deletion_manager = beat_frame.beat_deletion_manager

    def keyPressEvent(self, event: "QKeyEvent") -> None: 
        if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace:
            self.beat_deletion_manager.delete_selected_beat()
        else:
            super().keyPressEvent(event)  
