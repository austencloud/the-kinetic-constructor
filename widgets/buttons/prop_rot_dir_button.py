from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSignal

from constants import ICON_DIR
from PyQt6.QtGui import QIcon

from utilities.TypeChecking.TypeChecking import PropRotDirs


class PropRotDirButton(QPushButton):
    propRotDirChanged = pyqtSignal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setCheckable(True)
        self.prop_rot_dir: PropRotDirs = None
        self.clicked.connect(self.handle_click)

    def handle_click(self) -> None:
        if self.isChecked():
            self.propRotDirChanged.emit(self.prop_rot_dir)
        else:
            self.setChecked(True)  # Prevent unchecking by clicking the same button

    def setPropRotDir(self, direction: PropRotDirs) -> None:
        self.prop_rot_dir = direction
        self.setIcon(
            QIcon(f"{ICON_DIR}clock/{direction.lower()}_icon.png")
        ) 
