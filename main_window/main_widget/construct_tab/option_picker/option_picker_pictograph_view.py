from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from base_widgets.base_pictograph.bordered_pictograph_view import BorderedPictographView

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from .option_picker import OptionPicker

class OptionPickerPictographView(BorderedPictographView):

    def __init__(
        self, pictograph: "BasePictograph", option_picker: "OptionPicker"
    ) -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.pictograph.view = self
        self.option_picker = option_picker
        self.click_handler = self.option_picker.click_handler

    ### EVENTS ###

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.click_handler.on_option_clicked(self.pictograph)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        spacing = self.option_picker.scroll_area.spacing

        calculated_width = (self.option_picker.width() // 8) - spacing
        size = min(calculated_width, self.option_picker.height() // 8)

        border_width = max(1, int(size * 0.015))
        size -= 2 * border_width + spacing
        self.pictograph.view.update_border_widths()
        self.setFixedSize(size, size)
        self.view_scale = size / self.pictograph.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
