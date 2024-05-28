from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtGui import QImage, QFont
from widgets.sequence_widget.SW_beat_frame.beat import BeatView
from widgets.sequence_widget.SW_beat_frame.beat_drawer import BeatDrawer
from widgets.sequence_widget.SW_beat_frame.user_info_drawer import UserInfoDrawer
from widgets.sequence_widget.SW_beat_frame.word_drawer import WordDrawer

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.sequence_image_export_manager import (
        SequenceImageExportManager,
    )


class ImageDrawer:
    def __init__(self, export_manager: "SequenceImageExportManager"):
        self.export_manager = export_manager
