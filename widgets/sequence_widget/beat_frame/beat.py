from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)
from objects.pictograph.pictograph import Pictograph
from PyQt6.QtWidgets import QGraphicsView, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal, QObject

from objects.motion import Motion
from objects.pictograph.pictograph import Pictograph



if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.sequence_widget.beat_frame.beat_frame import BeatFrame


class Beat(Pictograph):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget, "beat")
        self.main_widget = main_widget


class BeatView(QGraphicsView):
    def __init__(self, beat_frame: "BeatFrame") -> None:
        super().__init__(beat_frame)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.pictograph: "Pictograph" = None
        self.beat: Beat = None

    def set_pictograph(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.setScene(self.pictograph)
        view_width = int(self.height() * 75 / 90)
        self.view_scale = view_width / self.pictograph.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton(QIcon(icon_path), "", self)
        button.clicked.connect(action)
        return button

    class BeatSignal(QObject):
        signal = pyqtSignal(Pictograph)
