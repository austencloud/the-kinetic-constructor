from widgets.base_widgets.base_rot_dir_button import BaseRotDirButton


class PropRotDirButton(BaseRotDirButton):
    def __init__(self, prop_rot_dir: str) -> None:
        super().__init__(prop_rot_dir)
        self.prop_rot_dir = prop_rot_dir
