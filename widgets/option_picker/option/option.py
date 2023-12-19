from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)
from objects.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt, QEvent
from typing import TYPE_CHECKING, Literal
from PyQt6.QtWidgets import QGraphicsView

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.option_picker.option_picker_scroll import OptionPickerScroll


class Option(Pictograph):
    def __init__(
        self,
        main_widget: "MainWidget",
        option_picker: "OptionPickerScroll",
        is_starter: bool = False,  # Set a default value for is_starter
    ) -> None:
        super().__init__(main_widget, "option")
        self.main_widget = main_widget
        self.is_starter = is_starter
        self.option_picker: OptionPickerScroll = option_picker
        self.setup_scene()
        self.setup_components(self.main_widget)
        self.view = OptionView(self)

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
        self.setMinimumHeight(int(view_width * 90 / 75))
        self.setMaximumHeight(int(view_width * 90 / 75))

        self.view_scale = view_width / self.option.width()

        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def wheelEvent(self, event):
        self.option.option_picker.wheelEvent(event)

    def eventFilter(self, obj, event: QEvent) -> Literal[False]:
        if event.type() == QEvent.Type.Wheel:
            event.ignore()
        return False
