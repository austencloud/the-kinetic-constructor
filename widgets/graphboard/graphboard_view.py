from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from widgets.graphboard.graphboard import GraphBoard

class GraphBoardView(QGraphicsView):
    def __init__(self, graphboard: 'GraphBoard') -> None:
        super().__init__()
        self.graphboard = graphboard
        main_window = self.graphboard.main_widget.main_window

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setScene(self.graphboard)
        
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.wheelEvent = lambda event: None
        
        # Adjust scaling based on new dimensions


        
        