from PyQt6.QtWidgets import QPushButton
from typing import Literal
from PyQt6.QtCore import QEvent
from PyQt6.QtCore import Qt
from constants.string_constants import CLOCKWISE, COUNTER_CLOCKWISE, ICON_DIR
from typing import TYPE_CHECKING
from PyQt6.QtGui import QIcon

from widgets.graph_editor.pictograph.pictograph_view import PictographView

if TYPE_CHECKING:
    from widgets.option_picker.option.option import Option


class OptionView(PictographView):
    def __init__(self, option: "Option") -> None:
        super().__init__(option)
        self.option = option

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setScene(self.option)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def init_buttons(self) -> None:
        self.rotate_cw_button = self.create_button(
            f"{ICON_DIR}rotate_cw.png",
            lambda: self.option.rotate_pictograph(CLOCKWISE),
        )
        self.rotate_ccw_button = self.create_button(
            f"{ICON_DIR}rotate_ccw.png",
            lambda: self.option.rotate_pictograph(COUNTER_CLOCKWISE),
        )

    def create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton(QIcon(icon_path), "", self)
        button.clicked.connect(action)
        return button

    def configure_button_size_and_position(self, button: QPushButton, size) -> None:
        pass

    def resizeEvent(self, event) -> None:
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

        button_size = int(self.width() / 7)
        self.configure_button_size_and_position(self.rotate_cw_button, button_size)
        self.configure_button_size_and_position(self.rotate_ccw_button, button_size)

    def wheelEvent(self, event):
        # Send the event to the OptionPicker's event filter
        self.option.option_picker.wheelEvent(event)


    def eventFilter(self, obj, event: QEvent) -> Literal[False]:
        if event.type() == QEvent.Type.Wheel:
            event.ignore()  # Ignore the event to let it propagate
        return False  # Return False to continue event propagation
