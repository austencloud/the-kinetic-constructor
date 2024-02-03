from PyQt6.QtWidgets import QPushButton
from utilities.TypeChecking.MotionAttributes import PropRotDirs
from utilities.TypeChecking.TypeChecking import VtgDirections



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

    def update_state_dict(self, state_dict: dict, value:bool) -> None:
        state_dict[self.direction] = value

    def press(self) -> None:
        self.setStyleSheet(self.get_button_style(pressed=True))

    def unpress(self) -> None:
        self.setStyleSheet(self.get_button_style(pressed=False))

class OpenCloseButton(RotDirButton):
    def __init__(self, open_close_state: VtgDirections) -> None:
        super().__init__(open_close_state)
        self.open_close_dir = open_close_state

class VtgDirButton(RotDirButton):
    def __init__(self, vtg_dir: VtgDirections) -> None:
        super().__init__(vtg_dir)
        self.vtg_dir = vtg_dir

class PropRotDirButton(RotDirButton):
    def __init__(self, prop_rot_dir: PropRotDirs) -> None:
        super().__init__(prop_rot_dir)
        self.prop_rot_dir = prop_rot_dir
