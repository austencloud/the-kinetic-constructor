from main_window.main_widget.sequence_builder.start_pos_picker.start_pos_picker_pictograph_view import (
    StartPosPickerPictographView,
)


class AdvancedStartPosPickerPictographView(StartPosPickerPictographView):
    def __init__(self, pictograph):
        super().__init__(pictograph)
        self.pictograph = pictograph

    def resizeEvent(self, event):
        """Override to prevent automatic resizing."""
