from base_widgets.base_rot_dir_button import BaseRotDirButton


class VtgDirButton(BaseRotDirButton):
    def __init__(self, vtg_dir: str) -> None:
        super().__init__(vtg_dir)
        self.vtg_dir = vtg_dir
