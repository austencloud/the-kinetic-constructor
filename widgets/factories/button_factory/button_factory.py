from PyQt6.QtGui import QIcon
from widgets.factories.button_factory.buttons.codex_adjust_turns_button import (
    CodexAdjustTurnsButton,
)
from widgets.factories.button_factory.buttons.rot_dir_buttons import (
    PropRotDirButton,
    VtgDirButton,
)
from widgets.factories.button_factory.buttons.swap_button import SwapButton


class ButtonFactory:
    @staticmethod
    def create_vtg_dir_button(icon_path: str, callback, vtg_dir) -> VtgDirButton:
        button = VtgDirButton(vtg_dir)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

    @staticmethod
    def create_prop_rot_dir_button(
        icon_path: str, callback, prop_rot_dir
    ) -> PropRotDirButton:
        button = PropRotDirButton(prop_rot_dir)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

    @staticmethod
    def create_swap_button(icon_path: str, callback: callable) -> "SwapButton":
        button = SwapButton(icon_path)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

    @staticmethod
    def create_adjust_turns_button(text: str) -> CodexAdjustTurnsButton:
        button = CodexAdjustTurnsButton()
        button.setText(text)
        return button
