

from PyQt5.QtWidgets import QMenu, QMenuBar, QAction, QDialog, QFormLayout, QSpinBox, QDialogButtonBox

class Context_Menu_Manager:
    def __init__(self, scene, sequence_manager, arrow_manipulator, exporter):
        self.scene = scene
        self.sequence_manager = sequence_manager
        self.arrow_manipulator = arrow_manipulator
        self.exporter = exporter

    def align_horizontally(self):
        items = self.scene().selectedItems()
        average_y = sum(item.y() for item in items) / len(items)
        for item in items:
            item.setY(average_y)

    def align_vertically(self):
        items = self.scene().selectedItems()
        average_x = sum(item.x() for item in items) / len(items)
        for item in items:
            item.setX(average_x)

