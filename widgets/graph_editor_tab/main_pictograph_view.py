from PyQt6.QtCore import Qt, QSize
from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QGraphicsView, QPushButton, QFrame
from PyQt6.QtGui import QIcon

from constants import CLOCKWISE, COUNTER_CLOCKWISE, ICON_DIR


if TYPE_CHECKING:
    from widgets.graph_editor_tab.main_pictograph import MainPictograph


class MainPictographView(QGraphicsView):
    def __init__(self, main_pictograph: "MainPictograph") -> None:
        super().__init__(main_pictograph)
        self.main_pictograph = main_pictograph

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setScene(self.main_pictograph)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.buttons = self.init_buttons()
        self.add_black_borders()

    def add_black_borders(self) -> None:
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setLineWidth(1)

    def init_buttons(self) -> List[QPushButton]:
        self.add_to_sequence_button = self.create_button(
            f"{ICON_DIR}add_to_sequence.png",
            self.main_pictograph.add_to_sequence_callback,
        )
        self.clear_button = self.create_button(
            f"{ICON_DIR}clear.png", self.main_pictograph.clear_pictograph
        )
        self.rotate_cw_button = self.create_button(
            f"{ICON_DIR}rotate_cw.png",
            lambda: self.main_pictograph.rotate_pictograph(CLOCKWISE),
        )
        self.rotate_ccw_button = self.create_button(
            f"{ICON_DIR}rotate_ccw.png",
            lambda: self.main_pictograph.rotate_pictograph(COUNTER_CLOCKWISE),
        )
        buttons = [
            self.add_to_sequence_button,
            self.clear_button,
            self.rotate_cw_button,
            self.rotate_ccw_button,
        ]
        return buttons

    def create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton(QIcon(icon_path), "", self)
        button.clicked.connect(action)
        return button

    def configure_button_size_and_position(self, button_size) -> None:
        for button in self.buttons:
            button.setMinimumSize(button_size, button_size)
            button.setMaximumSize(button_size, button_size)
            icon_size = int(button_size * 0.8)
            button.setIconSize(QSize(icon_size, icon_size))

            if button == self.add_to_sequence_button:
                button.move(self.width() - button_size, self.height() - button_size)
            elif button == self.clear_button:
                button.move(0, self.height() - button_size)
            elif button == self.rotate_cw_button:
                button.move(self.width() - button_size, 0)
            elif button == self.rotate_ccw_button:
                button.move(0, 0)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        button_size = int(self.width() / 10)
        self.configure_button_size_and_position(button_size)

        self.setMinimumHeight(int(self.main_pictograph.main_widget.height() * 0.3))
        self.setMaximumHeight(int(self.main_pictograph.main_widget.height() * 0.3))
        new_width = int(self.height())
        self.setMinimumWidth(new_width)
        self.setMaximumWidth(new_width)
        self.resetTransform()
        self.view_scale = min(
            self.width() / self.main_pictograph.sceneRect().width(),
            self.height() / self.main_pictograph.sceneRect().height(),
        )

        self.scale(
            self.view_scale,
            self.view_scale,
        )
        self.main_pictograph.view_scale = self.view_scale
        self.configure_button_size_and_position(int(self.width() / 10))
