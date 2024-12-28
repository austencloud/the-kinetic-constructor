from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QComboBox,
)
from PyQt6.QtCore import Qt

if TYPE_CHECKING:

    from main_window.main_widget.construct_tab.option_picker.option_picker_reversal_selector import (
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

        self.currentIndexChanged.connect(
            self.reversal_selector.option_picker.on_filter_changed
        )

    # on reswize, make the text bigger, a fraction of the width of the main widget
    def resizeEvent(self, event):
        super().resizeEvent(event)
        font = self.font()
        font_size = int(
            self.reversal_selector.option_picker.construct_tab.main_widget.width()
            * 0.01
        )
        font.setPointSize(font_size)
        font.setFamily("Georgia")
        self.setFont(font)
        self.setStyleSheet(
            f"""
            QComboBox {{
            background-color: white;
            color: black;
            border: 1px solid gray;
            padding: 2px 4px;
            font-size: {font_size}px;
            }}
            QComboBox QAbstractItemView {{
            background-color: white;
            color: black;
            selection-background-color: lightgray;
            selection-color: black;
            font-size: {font_size}px;
            }}
            QComboBox QAbstractItemView::item:hover {{
            background-color: lightblue;
            color: black;
            font-size: {font_size}px;
            }}
            QComboBox::drop-down {{
            border: none;
            }}
            QComboBox:hover {{
                border: 1px solid lightgray;
            }}
            QComboBox:focus {{
                border: 1px solid blue;
            }}
        """
        )
