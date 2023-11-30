from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QComboBox,
    QFrame, QVBoxLayout
)
from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class MotionTypesWidget(QWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)
        self.layout = QVBoxLayout(self)
        self.attr_box = attr_box
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # Add this line to center the contents

        # Type Label
        self.type_label = QLabel("Type", self)
        self.type_label.setFixedWidth(int(self.attr_box.attr_box_width / 5))
        self.type_label.setFont(QFont("Arial", 12))
        self.type_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        # Motion Type ComboBox
        self.type_combo_box = QComboBox(self)
        self.type_combo_box.addItems(["Pro", "Anti", "Dash", "Static"])
        self.type_combo_box.setStyleSheet(self.get_combo_box_style())
        self.type_combo_box.setFont(QFont("Arial", 20, QFont.Weight.Bold, italic=True))

        # Set the fixed size to maintain the size of the ComboBox

        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()
        
        button_frame = QFrame()
        spacer_frame = QFrame()

        bottom_layout.addWidget(button_frame)
        bottom_layout.addWidget(self.type_combo_box)
        bottom_layout.addWidget(spacer_frame)

        button_frame.setFixedWidth(int(self.attr_box.attr_box_width / 5))
        spacer_frame.setFixedWidth(int(self.attr_box.attr_box_width / 5))

        self.layout.addLayout(top_layout)
        self.layout.addLayout(bottom_layout)

        top_layout.addWidget(self.type_label)

    def get_combo_box_style(self) -> str:
        return (
            "QComboBox {"
            "   border: 2px solid black;"
            "   border-radius: 10px;"
            "}"
            "QComboBox::drop-down {"
            "   subcontrol-origin: padding;"
            "   subcontrol-position: top right;"
            "   width: 15px;"
            "   border-left-width: 1px;"
            "   border-left-color: darkgray;"
            "   border-left-style: solid;"
            "   border-top-right-radius: 3px;"
            "   border-bottom-right-radius: 3px;"
            "}"
            "QComboBox::down-arrow {"
            "   image: url('resources/images/icons/combobox_arrow.png');"
            "   width: 10px;"
            "   height: 10px;"
            "}"
        )

    def update_motion_type(self, motion_type) -> None:
        print(f"Motion type set to: {motion_type}")

    def update_motion_type_widget_size(self) -> None:
        self.setFixedSize(
            self.attr_box.attr_box_width,
            int(self.attr_box.height() * 1 / 6),
        )
