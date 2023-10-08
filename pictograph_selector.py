from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QLabel, QGraphicsScene
from mini_graphboard import Mini_Graphboard_View
from objects.grid import Grid

class Selection_Dialog(QDialog):
    def __init__(self, combinations, letter, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{letter} Variations:")
        
        layout = QVBoxLayout()
        grid_layout = QGridLayout()
        
        # Create a QLabel for the chosen letter
        letter_label = QLabel(f"{letter} Variations:")
        layout.addWidget(letter_label)
        
        row = 0
        col = 0
        for i, combination in enumerate(combinations):
            mini_graphboard = Mini_Graphboard_View()
            mini_graphboard.add_arrows_to_mini_graphboard(combination)
            grid_layout.addWidget(mini_graphboard, row, col)
                    
            col += 1
            if col >= 4:
                col = 0
                row += 1
        
        layout.addLayout(grid_layout)
        self.setLayout(layout)

    def select_pictograph(self):
        # TODO: Logic to get the selected pictograph and close the dialog
        self.accept()
        
