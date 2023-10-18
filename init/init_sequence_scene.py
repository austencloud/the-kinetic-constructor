from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView
from managers.sequence_manager import Sequence_Manager
from settings import GRAPHBOARD_HEIGHT, GRAPHBOARD_WIDTH
class Init_Sequence_Scene:
    def __init__(self, main_widget):
        self.init_sequence_scene(main_widget)
    
    def init_sequence_scene(self, main_widget):
        main_window = main_widget.main_window

        sequence_scene = QGraphicsScene()
        sequence_scene.setSceneRect(0, 0, main_window.width(), 1 * GRAPHBOARD_HEIGHT)
        sequence_manager = Sequence_Manager(sequence_scene, main_widget.generator, main_widget, main_widget.info_tracker)
        sequence_scene.manager = sequence_manager
        sequence_container = QGraphicsView(sequence_scene)
        sequence_container.setFixedSize(int(sequence_scene.sceneRect().width()), int(sequence_scene.sceneRect().height()))
        sequence_container.show()
        main_window.lower_layout.addWidget(sequence_container)
        clear_sequence_button = sequence_manager.get_clear_sequence_button()
        main_window.lower_layout.addWidget(clear_sequence_button)

        main_widget.sequence_manager = sequence_manager
        main_widget.sequence_scene = sequence_scene
        main_widget.sequence_container = sequence_container
        main_widget.clear_sequence_button = clear_sequence_button
