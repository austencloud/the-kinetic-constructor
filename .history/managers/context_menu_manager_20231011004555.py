

from PyQt5.QtWidgets import QMenu, QMenuBar, QAction, QDialog, QFormLayout, QSpinBox, QDialogButtonBox

class Context_Menu_Manager:
    def __init__(self, scene, sequence_manager, arrow_manipulator, exporter):
        self.scene = scene
        self.sequence_manager = sequence_manager
        self.arrow_manipulator = arrow_manipulator
        self.exporter = exporter
