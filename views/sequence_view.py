from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from managers.sequence_manager import Sequence_Manager
from settings import GRAPHBOARD_HEIGHT, GRAPHBOARD_WIDTH

class Sequence_View(QGraphicsView):
    def __init__(self, main_widget):
        super().__init__()
        main_window = main_widget.main_window

        sequence_scene = QGraphicsScene()
        sequence_scene.setSceneRect(0, 0, main_window.width(), 1 * GRAPHBOARD_HEIGHT * 2)
        sequence_manager = Sequence_Manager(sequence_scene, main_widget.generator, main_widget, main_widget.info_tracker)
        sequence_scene.manager = sequence_manager

        self.setFixedSize(int(sequence_scene.sceneRect().width()), int(sequence_scene.sceneRect().height()))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.show()
        
        main_widget.word_label = QLabel(main_widget.main_window)
        main_widget.main_window.lower_layout.addWidget(main_widget.word_label)
        main_widget.word_label.setFont(QFont('Helvetica', 20))
        main_widget.word_label.setText("My word: ")
        
        main_window.lower_layout.addWidget(self)
        clear_sequence_button = sequence_manager.get_clear_sequence_button()
        main_window.lower_layout.addWidget(clear_sequence_button)

        main_widget.sequence_manager = sequence_manager
        main_widget.sequence_scene = sequence_scene
        main_widget.sequence_view = self
        main_widget.clear_sequence_button = clear_sequence_button
