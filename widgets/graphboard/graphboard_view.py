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
        # Calculate view size based on window dimensions and aspect ratio
        view_height = main_window.width() * 0.30  # Example: 40% of window width
        view_width = view_height * 75 / 90  # Maintain 75:90 ratio

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setFixedSize(int(view_width), int(view_height))
        self.setScene(self.graphboard)
        
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.wheelEvent = lambda event: None
        
        # Adjust scaling based on new dimensions
        view_scale = view_width / self.graphboard.width()
        self.scale(view_scale, view_scale)
        

        
        