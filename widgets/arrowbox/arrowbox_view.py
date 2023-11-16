from PyQt6.QtWidgets import QGraphicsView, QFrame
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
if TYPE_CHECKING:   
    from widgets.arrowbox.arrowbox import ArrowBox
    
class ArrowBoxView(QGraphicsView):
    def __init__(self, arrowbox: 'ArrowBox') -> None:
        super().__init__(arrowbox)
        self.setFixedSize(
            int(arrowbox.main_window.width() * 0.1),
            int(arrowbox.main_window.width() * 0.1),
        )
        self.setScene(arrowbox)
        
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.scale(0.3, 0.3)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)