from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.sequence_image_export_manager import (
        SequenceImageExportManager,
    )


class ImageDrawer:
    def __init__(self, export_manager: "SequenceImageExportManager"):
        self.export_manager = export_manager
