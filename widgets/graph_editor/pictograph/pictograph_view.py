from PyQt6.QtWidgets import QGraphicsView, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from constants.string_constants import CLOCKWISE, COUNTER_CLOCKWISE, ICON_DIR
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph
from PyQt6.QtCore import QSize


class PictographView(QGraphicsView):
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setScene(self.pictograph)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.wheelEvent = lambda event: None

        # Initialize buttons
        self.init_buttons()

    def remove_buttons(self) -> None:
        self.add_to_sequence_button.deleteLater()
        self.clear_button.deleteLater()
        self.rotate_cw_button.deleteLater()
        self.rotate_ccw_button.deleteLater()

    def init_buttons(self) -> None:
        self.add_to_sequence_button = self.create_button(
            f"{ICON_DIR}add_to_sequence.png",
            self.pictograph.add_to_sequence_callback,
        )
        self.clear_button = self.create_button(
            f"{ICON_DIR}clear.png", self.pictograph.clear_pictograph
        )
        self.rotate_cw_button = self.create_button(
            f"{ICON_DIR}rotate_cw.png",
            lambda: self.pictograph.rotate_pictograph(CLOCKWISE),
        )
        self.rotate_ccw_button = self.create_button(
            f"{ICON_DIR}rotate_ccw.png",
            lambda: self.pictograph.rotate_pictograph(COUNTER_CLOCKWISE),
        )

    def create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton(QIcon(icon_path), "", self)
        button.clicked.connect(action)
        return button

    def configure_button_size_and_position(self, button: QPushButton, size) -> None:
        button.setFixedSize(size, size)
        icon_size = int(size * 0.8)
        button.setIconSize(QSize(icon_size, icon_size))

        # Custom positioning logic if needed
        if button == self.add_to_sequence_button:
            button.move(self.width() - size, self.height() - size)
        elif button == self.clear_button:
            button.move(0, self.height() - size)
        elif button == self.rotate_cw_button:
            button.move(self.width() - size, 0)
        elif button == self.rotate_ccw_button:
            button.move(0, 0)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        view_height = int(self.pictograph.graph_editor.height())
        view_width = int(view_height * 75 / 90)
        self.setMaximumHeight(view_height)
        self.setMinimumWidth(view_width)
        self.setMaximumWidth(view_width)
        self.pictograph.graph_editor.arrowbox.view.set_size_to_match_pictograph_view()
        self.pictograph.graph_editor.propbox.view.set_size_to_match_pictograph_view()
        self.pictograph.graph_editor.attr_panel.red_attr_box.set_size_to_match_pictograph_view()
        self.pictograph.graph_editor.attr_panel.blue_attr_box.set_size_to_match_pictograph_view()
        self.view_scale = min(
            view_width / self.pictograph.sceneRect().width(),
            view_height / self.pictograph.sceneRect().height(),
        )

        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

        if hasattr(self, "add_to_sequence_button"):
            self.update_button_size(view_width)

    def update_button_size(self, view_width) -> None:
        button_size = int(view_width / 7)
        self.configure_button_size_and_position(
            self.add_to_sequence_button, button_size
        )
        self.configure_button_size_and_position(self.clear_button, button_size)
        self.configure_button_size_and_position(self.rotate_cw_button, button_size)
        self.configure_button_size_and_position(self.rotate_ccw_button, button_size)
