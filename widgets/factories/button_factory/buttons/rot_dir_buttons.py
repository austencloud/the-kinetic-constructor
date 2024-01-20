from PyQt6.QtWidgets import QPushButton
from utilities.TypeChecking.TypeChecking import VtgDirections, PropRotDirs


class RotDirButton(QPushButton):
    def __init__(self, direction) -> None:
        super().__init__()
        self.direction = direction

    def get_button_style(self, pressed: bool) -> str:
        if pressed:
            return """
                QPushButton {
                    background-color: #ccd9ff;
                    border: 2px solid #555555;
                    border-bottom-color: #888888; /* darker shadow on the bottom */
                    border-right-color: #888888; /* darker shadow on the right */
                }
            """
        else:
            return """
                QPushButton {
                    background-color: white;
                    border: 1px solid black;
                }
                QPushButton:hover {
                    background-color: #e6f0ff;
                }
            """

    def press(self) -> None:
        self.setStyleSheet(self.get_button_style(pressed=True))

    def unpress(self) -> None:
        self.setStyleSheet(self.get_button_style(pressed=False))


class VtgDirButton(RotDirButton):
    def __init__(self, vtg_dir: VtgDirections) -> None:
        super().__init__(vtg_dir)
        self.vtg_dir = vtg_dir

class PropRotDirButton(RotDirButton):
    def __init__(self, prop_rot_dir: PropRotDirs) -> None:
        super().__init__(prop_rot_dir)
        self.prop_rot_dir = prop_rot_dir
