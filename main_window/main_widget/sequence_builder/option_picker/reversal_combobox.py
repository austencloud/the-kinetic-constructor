from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QComboBox,
)
from PyQt6.QtCore import Qt

if TYPE_CHECKING:

    from main_window.main_widget.sequence_builder.option_picker.option_picker_reversal_selector import (
        OptionPickerReversalSelector,
    )


class ReversalCombobox(QComboBox):
    def __init__(self, reversal_selector: "OptionPickerReversalSelector"):
        super().__init__(reversal_selector)
        self.reversal_selector = reversal_selector

        self.addItem("All", userData=None)
        self.addItem("Continuous", userData="continuous")
        self.addItem("One Reversal", userData="one_reversal")
        self.addItem("Two Reversals", userData="two_reversals")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(
            """
            QComboBox {
            background-color: white;
            color: black;
            border: 1px solid gray;
            padding: 2px 4px;
            }
            QComboBox QAbstractItemView {
            background-color: white;
            color: black;
            selection-background-color: lightgray;
            selection-color: black;
            }
            QComboBox QAbstractItemView::item:hover {
            background-color: lightblue;
            color: black;
            }
            QComboBox::drop-down {
            border: none;
            }
            QComboBox::down-arrow {
                image: url(arrow_down_icon.png); /* Replace with your icon */
                width: 10px;
                height: 10px;
            }
            QComboBox:hover {
                border: 1px solid lightgray;
            }
            QComboBox:focus {
                border: 1px solid blue;
            }
        """
        )
        self.currentIndexChanged.connect(
            self.reversal_selector.option_picker.on_filter_changed
        )
