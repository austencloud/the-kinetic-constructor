from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont
from typing import Union, TYPE_CHECKING


if TYPE_CHECKING:
    from ..filter_frame.attr_box.attr_box_widgets.header_widgets.base_header_widget import (
        HeaderWidget,
    )
    from ..filter_frame.attr_box.attr_box_widgets.motion_types_widget import (
        MotionTypeWidget,
    )
    from ..filter_frame.attr_box.attr_box_widgets.start_end_loc_widget import (
        StartEndLocWidget,
    )
    from ..filter_frame.attr_box.attr_box_widgets.turns_widgets.base_turns_widget.base_turns_widget import (
        TurnsWidget,
    )
from PyQt6.QtGui import QIcon

class VtgDirButton(QPushButton):
    def __init__(
        self,
        parent_widget: Union[
            "StartEndLocWidget", "TurnsWidget", "MotionTypeWidget", "HeaderWidget"
        ],
    ) -> None:
        super().__init__(parent_widget)
        self.parent_widget = parent_widget
        
    def get_vtg_dir_button_style(self, pressed: bool) -> str:
        if pressed:
            return """
                QPushButton {
                    background-color: #ccd9ff;
                    border: 2px solid #555555;
                    border-bottom-color: #888888; /* darker shadow on the bottom */
                    border-right-color: #888888; /* darker shadow on the right */
                    padding: 5px;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: white;
                    border: 1px solid black;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #e6f0ff;
                }
            """

    def press(self) -> None:
        self.setStyleSheet(self.get_vtg_dir_button_style(pressed=True))

    def unpress(self) -> None:
        self.setStyleSheet(self.get_vtg_dir_button_style(pressed=False))

    def is_pressed(self) -> bool:
        return self.styleSheet() == self.get_vtg_dir_button_style(pressed=True)
    
    def is_unpressed(self) -> bool:
        return self.styleSheet() == self.get_vtg_dir_button_style(pressed=False)