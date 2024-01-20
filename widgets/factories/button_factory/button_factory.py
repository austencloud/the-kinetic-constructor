from PyQt6.QtGui import QIcon
from constants import ICON_DIR
from widgets.factories.button_factory.buttons.rot_dir_buttons import PropRotDirButton, VtgDirButton

class ButtonFactory:
    @staticmethod
    def create_vtg_dir_button(icon_path: str, callback, vtg_dir) -> VtgDirButton:
        button = VtgDirButton(vtg_dir)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

    @staticmethod
    def create_prop_rot_dir_button(icon_path: str, callback, prop_rot_dir) -> PropRotDirButton:
        button = PropRotDirButton(prop_rot_dir)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button
