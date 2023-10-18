from PyQt6.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor
from views.pictograph_view import Pictograph_View

class Pictograph_Selector(QDialog):
    def __init__(self, combinations, letter, main_graphboard_view, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{letter} Variations:")
        
        layout = QVBoxLayout()
        grid_layout = QGridLayout()
        letter_label = QLabel(f"{letter} Variations:")
        letter_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        letter_label.setFont(font)
        layout.addWidget(letter_label)
        
        
        row = 0
        col = 0
        for i, combination in enumerate(combinations):
            pictograph = Pictograph_View(main_graphboard_view)
            pictograph.populate_pictograph(combination)
            grid_layout.addWidget(pictograph, row, col)
                    
            col += 1
            if col >= 4:
                col = 0
                row += 1
        
        layout.addLayout(grid_layout)
        self.setLayout(layout)

    def select_pictograph(self):
        # TODO: Logic to get the selected pictograph and close the dialog
        self.accept()
        

