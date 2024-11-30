from main_window.main_widget.sequence_builder.start_pos_picker.start_pos_picker_pictograph_view import (
    StartPosPickerPictographView,
)


class AdvancedStartPosPickerPictographView(StartPosPickerPictographView):
    def resizeEvent(self, event):
        """Override to prevent automatic resizing."""
        super().resizeEvent(event)
        # Do not call _resize_pictograph_view to prevent resizing
