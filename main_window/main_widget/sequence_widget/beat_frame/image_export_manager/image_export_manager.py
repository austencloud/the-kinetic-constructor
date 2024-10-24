from typing import TYPE_CHECKING

from main_window.main_widget.act import Act


from .image_export_layout_handler import ImageExportLayoutHandler
from .image_creator.image_creator import ImageCreator
from .image_export_beat_factory import ImageExportBeatFactory
from .image_export_dialog.image_export_dialog_executor import ImageExportDialogExecutor
from .image_saver import ImageSaver


if TYPE_CHECKING:
    from base_widgets.base_beat_frame import BaseBeatFrame


from typing import TYPE_CHECKING


class ImageExportManager:
    last_save_directory = None
    include_start_pos: bool

    def __init__(
        self,
        beat_frame: "BaseBeatFrame",
        beat_frame_class: type,
    ) -> None:
        self.beat_frame = beat_frame
        self.main_widget = beat_frame.main_widget
        if beat_frame_class.__name__ == "SequenceWidgetBeatFrame":
            self.sequence_widget = beat_frame.sequence_widget
        elif beat_frame_class.__name__ == "TempBeatFrame":
            self.dictionary_widget = beat_frame.dictionary_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.include_start_pos = (
            self.settings_manager.image_export.get_image_export_setting(
                "include_start_position"
            )
        )
        self.layout_handler = ImageExportLayoutHandler(self)
        self.beat_factory = ImageExportBeatFactory(self, beat_frame_class)
        self.image_creator = ImageCreator(self)
        self.image_saver = ImageSaver(self)
        self.dialog_executor = ImageExportDialogExecutor(self)

    def create_act_image(self, act: "Act"):
        # Similar to create_sequence_image but for the entire act
        pass