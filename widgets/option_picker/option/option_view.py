from PyQt6.QtWidgets import QGraphicsView, QPushButton
from PyQt6.QtCore import Qt
from settings.string_constants import CLOCKWISE, COUNTER_CLOCKWISE, ICON_DIR
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.option_picker.option.option import Option


class OptionView(QGraphicsView):
    def __init__(self, option: "Option") -> None:
        super().__init__()
        self.option = option

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setScene(self.option)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.wheelEvent = lambda event: None
        
    def update_OptionView_size(self) -> None:
        view_width = int((self.option.option_picker.width() / 4) - self.option.option_picker.spacing)
        
        self.setFixedWidth(view_width)
        self.setFixedHeight(int(view_width * 90/75))
        
        self.view_scale = view_width / self.option.width()
        
    
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
