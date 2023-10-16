from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QPushButton
from managers.sequence_manager import Sequence_Manager

class Init_Sequence_Scene:
    def __init__(self, ui_setup):
        self.init_sequence_scene(ui_setup)
    
    def init_sequence_scene(self, ui_setup):
        ui_setup.sequence_scene = QGraphicsScene()
        ui_setup.sequence_scene.setSceneRect(0, 0, 4 * 375, 375)
        ui_setup.sequence_manager = Sequence_Manager(ui_setup.sequence_scene, ui_setup.generator, ui_setup, ui_setup.info_tracker)
        ui_setup.sequence_scene.manager = ui_setup.sequence_manager
        ui_setup.sequence_container = QGraphicsView(ui_setup.sequence_scene)
        ui_setup.sequence_container.setFixedSize(1960, 500)
        ui_setup.sequence_container.show()
        ui_setup.main_window.lower_layout.addWidget(ui_setup.sequence_container)
        clear_sequence_button = ui_setup.sequence_manager.get_clear_sequence_button()
        ui_setup.main_window.lower_layout.addWidget(clear_sequence_button)

