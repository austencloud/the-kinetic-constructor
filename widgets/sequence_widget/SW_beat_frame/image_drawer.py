from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.image_export_manager import (
        ImageExportManager,
    )


class ImageDrawer:
    def __init__(self, export_manager: "ImageExportManager"):
        self.export_manager = export_manager
