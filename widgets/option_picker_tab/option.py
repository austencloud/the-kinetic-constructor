from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)
from objects.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt, QEvent
from typing import TYPE_CHECKING, Literal
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.option_picker_tab.option_picker_scroll import OptionPickerScroll


class Option(Pictograph):
    def __init__(
        self, main_widget: "MainWidget", option_picker: "OptionPickerScroll"
    ) -> None:
        super().__init__(main_widget, "option")
        self.main_widget = main_widget
        self.option_picker = option_picker
        self.imageLoaded = False
        self.pixmapItem = None  # Store the pixmap item
        self.pd_row_data = None  # Store the row data from the pandas dataframe

    def loadImage(self, image_path: str):
        """Load image from the path."""
        # Lazy loading: Only load the image if it's not already loaded and the view is visible
        if not self.imageLoaded and self.view.isVisible():
            # Caching: Check if the image is already cached
            cached_pixmap = self.option_picker.get_cached_pixmap(image_path)
            if cached_pixmap:
                pixmap = cached_pixmap
            else:
                pixmap = QPixmap(image_path)
                self.option_picker.cache_pixmap(image_path, pixmap)

            # Pixmap Item Reuse: Update existing pixmap item if it exists, otherwise create a new one
            if not self.pixmapItem:
                self.pixmapItem = QGraphicsPixmapItem(pixmap)
                self.addItem(self.pixmapItem)
            else:
                self.pixmapItem.setPixmap(pixmap)

            self.imageLoaded = True

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
            self.option.option_picker.width() / 4
        ) - self.option.option_picker.spacing * (
            self.option.option_picker.COLUMN_COUNT - 1
        )

        self.setMinimumWidth(view_width)
        self.setMaximumWidth(view_width)
        self.setMinimumHeight(view_width)
        self.setMaximumHeight(view_width)
        self.view_scale = view_width / self.option.width()

        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def wheelEvent(self, event):
        self.option.option_picker.wheelEvent(event)

    def eventFilter(self, obj, event: QEvent) -> Literal[False]:
        if event.type() == QEvent.Type.Wheel:
            event.ignore()
        return False

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.option.option_picker.load_image_if_visible(self.option)

    def showEvent(self, event):
        super().showEvent(event)
        self.option.option_picker.load_image_if_visible(self.option)
