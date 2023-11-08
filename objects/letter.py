from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from data.positions_map import positions_map
from data.letter_types import letter_types
class Letter():
    def __init__(self, graphboard):
        self.graphboard = graphboard
        super().__init__()

