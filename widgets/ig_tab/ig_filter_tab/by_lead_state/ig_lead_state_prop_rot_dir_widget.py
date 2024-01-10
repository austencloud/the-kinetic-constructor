from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from typing import TYPE_CHECKING
from constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    LEADING,
    NO_ROT,
)


from widgets.attr_box_widgets.base_rot_dir_widget import BaseRotDirWidget

if TYPE_CHECKING:
    from widgets.ig_tab.ig_filter_tab.by_lead_state.ig_lead_state_attr_box import (
        IGLeadStateAttrBox,
    )


class IGLeadStatePropRotDirWidget(BaseRotDirWidget):
    def __init__(self, attr_box: "IGLeadStateAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.initialize_ui()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_vbox_layout = QVBoxLayout()
        self.main_vbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

    def initialize_ui(self) -> None:
        self._setup_layout()
        self._setup_rot_dir_widget()


    def _create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton("", self)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(button.size())
        button.clicked.connect(action)
        button.setContentsMargins(0, 0, 0, 0)
        return button


    def _setup_header_label(self) -> QLabel:
        text = "Leading" if self.attr_box.lead_state == LEADING else "Trailing"
        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"font-weight: bold;")
        return label



    ### EVENT HANDLERS ###

    def update_button_size(self) -> None:
        button_size = self.width() // 3
        for prop_rot_dir_button in self.prop_rot_dir_buttons:
            prop_rot_dir_button.setMinimumSize(button_size, button_size)
            prop_rot_dir_button.setMaximumSize(button_size, button_size)
            prop_rot_dir_button.setIconSize(prop_rot_dir_button.size() * 0.9)

    def resize_prop_rot_dir_widget(self) -> None:
        self.update_button_size()

    def _get_current_prop_rot_dir(self) -> str:
        return (
            CLOCKWISE
            if self.attr_box.prop_rot_dir_widget.cw_button.isChecked()
            else COUNTER_CLOCKWISE
            if self.attr_box.prop_rot_dir_widget.ccw_button.isChecked()
            else NO_ROT
        )