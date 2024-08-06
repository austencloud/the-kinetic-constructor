from typing import TYPE_CHECKING, Union
from widgets.image_export_layout_handler import ImageExportLayoutHandler

from widgets.sequence_widget.SW_beat_frame.image_creator import ImageCreator
from widgets.sequence_widget.SW_beat_frame.image_export_beat_factory import (
    ImageExportBeatFactory,
)
from widgets.sequence_widget.SW_beat_frame.image_export_dialog_executor import (
    ImageExportDialogExecutor,
)
from widgets.sequence_widget.SW_beat_frame.image_saver import ImageSaver

if TYPE_CHECKING:
    from widgets.dictionary_widget.temp_beat_frame import (
        TempBeatFrame,
    )
    from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import SW_BeatFrame


from typing import TYPE_CHECKING


class ImageExportManager:
    last_save_directory = None
    include_start_pos: bool

    def __init__(
        self,
        beat_frame: Union["SW_BeatFrame", "TempBeatFrame"],
        beat_frame_class: type,
    ) -> None:
        self.beat_frame = beat_frame
        self.main_widget = beat_frame.main_widget
        if beat_frame_class.__name__ == "SW_BeatFrame":
            self.sequence_widget = beat_frame.sequence_widget
        elif beat_frame_class.__name__ == "InvisibleDictionaryBeatFrame":
            self.dictionary_widget = beat_frame.dictionary_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.include_start_pos = (
            self.settings_manager.image_export.get_image_export_setting(
                "include_start_position", True
            )
        )
        self.layout_handler = ImageExportLayoutHandler(self)
        self.beat_factory = ImageExportBeatFactory(self, beat_frame_class)
        self.image_creator = ImageCreator(self)
        self.image_saver = ImageSaver(self)
        self.dialog_executor = ImageExportDialogExecutor(self)
