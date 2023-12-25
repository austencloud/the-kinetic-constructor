import os
from typing import TYPE_CHECKING, Literal
from PyQt6.QtCore import Qt, QEvent, QByteArray, QBuffer, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QImage, QPainter
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from Enums import *
from utilities.TypeChecking.TypeChecking import TYPE_CHECKING
from objects.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.option_picker_tab.option_picker_scroll_area import (
        OptionPickerScrollArea,
    )


class Option(Pictograph):
    imageGenerated = pyqtSignal(str)  # Signal to indicate when an image is generated

    ### INIT ###

    def __init__(
        self, main_widget: "MainWidget", option_picker_scroll: "OptionPickerScrollArea"
    ) -> None:
        self.view: "OptionView" = None
        super().__init__(main_widget, "option")
        self.main_widget = main_widget
        self.option_picker_scroll = option_picker_scroll

    ### IMAGE LOADING ###

    def loadImage(self, image_path: str) -> None:
        """Load image from the path."""
        # Lazy loading: Only load the image if it's not already loaded and the view is visible
        if not self.image_loaded and self.view.isVisible():
            # Caching: Check if the image is already cached
            cached_pixmap = self.option_picker_scroll.get_cached_pixmap(image_path)
            if cached_pixmap:
                pixmap = cached_pixmap
            else:
                pixmap = QPixmap(image_path)
                self.main_widget.cache_pixmap(image_path, pixmap)

            # Pixmap Item Reuse: Update existing pixmap item if it exists, otherwise create a new one
            if not self.pixmap:
                self.pixmap = QGraphicsPixmapItem(pixmap)
                self.addItem(self.pixmap)
            else:
                self.pixmap.setPixmap(pixmap)

            self.image_loaded = True

    ### EVENTS ###

    def wheelEvent(self, event) -> None:
        return super().wheelEvent(event)


class OptionView(QGraphicsView):
    def __init__(self, option: "Option") -> None:
        super().__init__(option)
        self.option = option

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setScene(self.option)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def resize_option_view(self) -> None:
        view_width = int(
            self.option.option_picker_scroll.width() / 4
        ) - self.option.option_picker_scroll.spacing * (
            self.option.option_picker_scroll.COLUMN_COUNT - 1
        )

        self.setMinimumWidth(view_width)
        self.setMaximumWidth(view_width)
        self.setMinimumHeight(view_width)
        self.setMaximumHeight(view_width)
        self.view_scale = view_width / self.option.width()

        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def wheelEvent(self, event):
        self.option.option_picker_scroll.wheelEvent(event)

    def eventFilter(self, obj, event: QEvent) -> Literal[False]:
        if event.type() == QEvent.Type.Wheel:
            event.ignore()
        return False

    def showEvent(self, event):
        super().showEvent(event)
        # Ensure this slot is called after the event loop starts
        QTimer.singleShot(0, self.option.load_image_if_needed)
