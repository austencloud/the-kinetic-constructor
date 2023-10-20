from PyQt6.QtWidgets import (
    QGraphicsScene, QGraphicsView, QGridLayout, QWidget, 
    QVBoxLayout, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
# Import other necessary modules

class Optionboard_View(QGraphicsView):
    def __init__(self, main_widget):
        super().__init__()

        self.main_widget = main_widget  # Store reference to the main widget

        # Create a widget that will contain the grid layout
        self.optionboard_scene = QGraphicsScene()
        # self.setScene(self.optionboard_scene)  # Set the scene
        self.grid_widget = QWidget()
        self.optionboard_grid_layout = QGridLayout()
        self.grid_widget.setLayout(self.optionboard_grid_layout)

        # Populate the grid layout with pictographs (placeholder buttons for now)
        self.populate_pictographs()

        #disable teh scrollbars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.optionboard_scene.setSceneRect(0, 0, 600, 800)

        # Create a scroll area and set it to contain the grid widget
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Ensure the widget resizes inside the scroll area
        self.scroll_area.setWidget(self.grid_widget)

        # Create a main layout and add the scroll area to it
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scroll_area)

        # Set the main layout on a container widget
        self.container_widget = QWidget()
        self.container_widget.setLayout(self.main_layout)
        #set the size
        self.container_widget.setFixedSize(600, 800)

        # Set the QGraphicsScene and add the container widget to it
        self.optionboard_scene = QGraphicsScene()
        self.optionboard_scene.addWidget(self.container_widget)

        self.setScene(self.optionboard_scene)
        self.setFixedSize(int(self.optionboard_scene.sceneRect().width()), int(self.optionboard_scene.sceneRect().height()))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # Enable the vertical scrollbar

        self.show()

    def populate_pictographs(self):
        # This method will populate the grid with pictographs. 
        # For now, we're using placeholder buttons. You'll replace this with actual pictographs.
        number_of_pictographs = 50  # Just a placeholder value for demonstration

        MAX_ITEMS_PER_ROW = 4  # Set the maximum number of pictographs per row

        for i in range(number_of_pictographs):
            # Create a button to represent the pictograph (this is a placeholder)
            pictograph_button = QPushButton(f"Picto {i+1}")
            pictograph_button.setIcon(QIcon(QPixmap("path/to/your/pictograph/image")))  # Set the pictograph image here
            pictograph_button.setIconSize(QSize(100, 100))  # Or any appropriate size for your pictographs
            pictograph_button.setFixedSize(125, 150)  # Set the button width and height
            pictograph_button.clicked.connect(self.on_pictograph_clicked)

            # Calculate the row and column index
            row = i // MAX_ITEMS_PER_ROW  # Adjusted to 4 pictographs per row
            col = i % MAX_ITEMS_PER_ROW

            # Add the button to the grid layout
            self.optionboard_grid_layout.addWidget(pictograph_button, row, col)


    def on_pictograph_clicked(self):
        # This method will handle the logic when a pictograph is clicked.
        # For now, it's just a placeholder.
        print("Pictograph clicked!")  # Placeholder action
