from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSizePolicy, QApplication, QMenu
from PyQt6.QtCore import Qt, QEvent, QTimer
from PyQt6.QtGui import QMouseEvent, QCursor, QKeyEvent, QAction, QContextMenuEvent

from base_widgets.base_pictograph.bordered_pictograph_view import BorderedPictographView
from base_widgets.base_pictograph.pictograph_context_menu_handler import (
    PictographContextMenuHandler,
)
from base_widgets.base_pictograph.pictograph_view_key_event_handler import (
    PictographViewKeyEventHandler,
)


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from main_window.main_widget.construct_tab.option_picker.option_picker import (
        OptionPicker,
    )


class OptionPickerPictographView(BorderedPictographView):
    original_style: str

    def __init__(
        self, pictograph: "BasePictograph", option_picker: "OptionPicker"
    ) -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph
        self.pictograph.view = self
        self.option_picker = option_picker
        self.original_style = ""


    ### EVENTS ###

    def mousePressEvent(self, event: QMouseEvent) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if event.button() == Qt.MouseButton.LeftButton:
            self.pictograph.main_widget.construct_tab.option_picker.click_handler.on_option_clicked(
                self.pictograph
            )
        QApplication.restoreOverrideCursor()

    def enterEvent(self, event: QEvent) -> None:
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pictograph.view.set_gold_border()

    def leaveEvent(self, event: QEvent) -> None:
        self.setStyleSheet("")
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.pictograph.view.reset_border()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        size = self.calculate_view_size()
        self.pictograph.view.update_border_widths()
        self.setMinimumWidth(size)
        self.setMaximumWidth(size)
        self.setMinimumHeight(size)
        self.setMaximumHeight(size)
        self.view_scale = size / self.pictograph.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def calculate_view_size(self) -> int:
        spacing = self.option_picker.scroll_area.spacing

        calculated_width = int(
            (self.pictograph.main_widget.construct_tab.option_picker.width() / 8)
            - spacing
        )

        view_width = (
            calculated_width
            if calculated_width
            < self.pictograph.main_widget.construct_tab.option_picker.height() // 8
            else self.pictograph.main_widget.construct_tab.option_picker.height() // 8
        )

        outer_border_width = max(1, int(view_width * 0.015))
        inner_border_width = max(1, int(view_width * 0.015))

        view_width = view_width - (outer_border_width) - (inner_border_width) - spacing

        return view_width
