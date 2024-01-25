from PyQt6.QtGui import QIcon
from widgets.factories.button_factory.buttons.rot_dir_buttons import OpenCloseButton, PropRotDirButton, VtgDirButton
from widgets.letter_button_frame.components.letter_button import LetterButton

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

    def create_open_close_button(icon_path: str, callback, open_close_state) -> OpenCloseButton:
        button = OpenCloseButton(open_close_state)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

    @staticmethod
    def create_letter_button(icon_path, letter_str: str, letter_type: str) -> LetterButton:
        button = LetterButton(icon_path, letter_str)
        return button

