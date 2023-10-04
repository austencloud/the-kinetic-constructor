from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QDialog, QGraphicsView, QGraphicsScene, QVBoxLayout, QPushButton, QGraphicsItem, QGridLayout, QLabel

class Pictograph(QGraphicsItem):
    def __init__(self, state, image: QImage, parent=None):
        super().__init__(parent)
        self.state = state
        self.image = image
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        
    def paint(self, painter: QPainter, option, widget):
        # Scale the image to fit the rectangle while preserving aspect ratio
        scaled_image = self.image.scaled(450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # Render the QImage onto the Pictograph
        painter.drawImage(QRectF(0, 0, scaled_image.width(), scaled_image.height()), scaled_image)

    def boundingRect(self):
        # Return the bounding rectangle of the Pictograph
        return QRectF(0, 0, 375, 375)

    def mousePressEvent(self, event):
        # Emit the clicked signal when the Pictograph is clicked
        event.accept()

class Pictograph_Selector(QDialog):
    def __init__(self, combinations, letter, graphboard_view, parent=None):
        super().__init__(parent)
        self.letter = letter
        self.graphboard_view = graphboard_view
        # Create a grid layout
        grid_layout = QGridLayout()
        # Add the label for the chosen letter
        letter_label = QLabel(f"{letter} Variations:")
        letter_label.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(letter_label, 0, 0, 1, 4)  # Span 4 columns
        
        original_width = self.graphboard_view.width()
        original_height = self.graphboard_view.height()
        
        # Create and add mini graphboards to the grid layout
        row = 1
        col = 0
        for combination in combinations:
            mini_graphboard = QGraphicsView()  # Replace with your actual mini graphboard
            mini_graphboard.setFixedSize(0.4 * original_width, 0.4 * original_height)
            
            grid_layout.addWidget(mini_graphboard, row, col)
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        self.setLayout(grid_layout)
    
    def select_pictograph(self):
        # TODO: Logic to get the selected pictograph and close the dialog
        self.accept()
        
    def showEvent(self, event):
        # Resize the dialog to fit the contents
        self.resize(self.layout.sizeHint())
        super().showEvent(event)