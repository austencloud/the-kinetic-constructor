from typing import TYPE_CHECKING, Literal
from PyQt6.QtCore import Qt, QEvent, pyqtSignal
from PyQt6.QtWidgets import QGraphicsView
from constants import OPTION
from utilities.TypeChecking.TypeChecking import TYPE_CHECKING
from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
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
        super().__init__(main_widget, OPTION)
        self.main_widget = main_widget
        self.option_picker_scroll = option_picker_scroll

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
        ) - self.option.option_picker_scroll.display_manager.SPACING * (
            self.option.option_picker_scroll.display_manager.COLUMN_COUNT - 1
        )

        self.setMinimumWidth(view_width)
        self.setMaximumWidth(view_width)
        self.setMinimumHeight(view_width)
        self.setMaximumHeight(view_width)
        self.view_scale = view_width / self.option.width()

        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def wheelEvent(self, event) -> None:
        self.option.option_picker_scroll.wheelEvent(event)

    def eventFilter(self, obj, event: QEvent) -> Literal[False]:
        if event.type() == QEvent.Type.Wheel:
            event.ignore()
        return False
