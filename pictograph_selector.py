from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QLabel, QGraphicsScene
from mini_graphboard import Mini_Graphboard
from grid import Grid

class Pictograph_Selector(QDialog):
    def __init__(self, combinations, letter, graphboard_view, graphboard_scene, grid, info_tracker, staff_manager, svg_handler, arrow_handler, ui_setup, generator, sequence_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{letter} Variations:")
        
        layout = QVBoxLayout()
        grid_layout = QGridLayout()
        
        main_graphboard_width = graphboard_view.width()
        main_graphboard_height = graphboard_view.height()
        
        # Create a QLabel for the chosen letter
        letter_label = QLabel(f"{letter} Variations:")
        layout.addWidget(letter_label)
        
        row = 0
        col = 0
        for i, combination in enumerate(combinations):

            mini_graphboard_scene = QGraphicsScene()
            mini_grid = Grid("images/grid.svg")

                
            mini_graphboard = Mini_Graphboard(mini_graphboard_scene, mini_grid, info_tracker, staff_manager, svg_handler, arrow_handler, ui_setup, generator, sequence_manager)
            mini_graphboard.populate_with_combination(combination)
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
        
