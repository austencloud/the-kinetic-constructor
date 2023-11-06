from PyQt6.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from objects.pictograph.pictograph_view import PictographView

class PictographSelectorDialog(QDialog):
    def __init__(self, main_widget, letter):
        super().__init__(main_widget)
        self.main_widget = main_widget
        letters = main_widget.letters
        self.letters = letters
        self.show_dialog(letter)
        
    def show_dialog(self, letter):
        combinations = self.letters.get(letter, [])
        if not combinations:
            return


        self.setWindowTitle(f"{letter} Variations:")
        layout = QVBoxLayout()
        grid_layout = QGridLayout()
                # Clear the previous widgets from the layout before adding new ones
        self.clear_layout(layout)  # Clear the main layout
        self.clear_layout(grid_layout)  # Clear the grid layout if it's reused

        
        letter_label = QLabel(f"{letter} Variations:")
        letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        letter_label.setFont(font)
        layout.addWidget(letter_label)
        
        row = 0
        col = 0
        for i, combination in enumerate(combinations):
            pictograph = PictographView(self.main_widget)
            pictograph.populate_pictograph(combination)
            grid_layout.addWidget(pictograph, row, col)
                    
            col += 1
            if col >= 4:
                col = 0
                row += 1
        
        layout.addLayout(grid_layout)
        self.setLayout(layout)
        self.show()

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def select_pictograph(self):
        result = self.exec()
        
        if result == QDialog.accepted:
            # TODO: Handle the selected pictograph
            pass
        
        # TODO: Logic to get the selected pictograph and close the dialog
        self.accept()
        
