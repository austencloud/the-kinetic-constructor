from PyQt6.QtWidgets import QGraphicsView, QFrame
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
if TYPE_CHECKING:   
    from widgets.arrowbox.arrowbox import ArrowBox
    
class ArrowBoxView(QGraphicsView):
    def __init__(self, arrowbox: 'ArrowBox') -> None:
        super().__init__(arrowbox)
        self.setFixedSize(
            int(arrowbox.main_window.height() * 1/6),
            int(arrowbox.main_window.height() * 1/6),
        )
        self.setScene(arrowbox)
        
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.arrowbox = arrowbox
        self.scene_width = self.arrowbox.main_window.width() / 9
        
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        
    def resizeEvent(self, event):
        super().resizeEvent(event)  # Call the parent class's resizeEvent
        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.scale(self.width() / self.scene_width, self.width() / self.scene_width)
