from PyQt6.QtWidgets import (
    QScrollArea,
    QSizePolicy,
    QFrame,
    QWidget,
    QGridLayout,
    QPushButton,
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.option_picker.option_picker import OptionPicker


class ScrollArea(QScrollArea):
    """
    A custom scroll area widget for the option picker.
    """

    def __init__(self, option_picker: "OptionPicker") -> None:
        """
        Initialize the OptionPickerScrollArea.

        Args:
            option_picker (OptionPicker): The parent OptionPicker widget.
        """
        super().__init__()
        self.main_window = option_picker.main_window
        self.main_widget = option_picker.main_widget
        self.option_picker = option_picker
        self.scrollbar_width = 0  # Class variable to store the width of the scrollbar
        self.spacing = 16  # Class variable to store the spacing between pictographs
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setWidgetResizable(True)
        self.grid_widget = QWidget()
        self.option_picker_grid_layout = QGridLayout(self.grid_widget)
        self.option_picker_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.option_picker_grid_layout.setSpacing(self.spacing)
        self.setWidget(
            self.grid_widget
        )  # Set the grid widget as the widget for the scroll area
        # Assuming the width of the OptionBoard (self.width()) is available
        # According to the desired ratio
        # set the vertical scrol bar's width
        self.verticalScrollBar().setFixedWidth(int(self.main_window.width() * 0.01))
        self.populate_pictographs()
        self.connect_signals()
        self.update_scroll_area_size()

    def connect_signals(self) -> None:
        """
        Connect the clicked signal of each pictograph button to the on_pictograph_clicked slot.
        """
        for button in self.grid_widget.findChildren(QPushButton):
            button.clicked.connect(self.on_pictograph_clicked)

    def populate_pictographs(self) -> None:
        """
        Populate the scroll area with pictograph buttons.
        """

        number_of_pictographs = 50
        MAX_ITEMS_PER_ROW = 4
        for i in range(number_of_pictographs):
            pictograph_button = QPushButton(f"Picto {i+1}")
            pictograph_button.setIcon(QIcon(QPixmap("path/to/your/pictograph/image")))

            self.option_picker_grid_layout.addWidget(
                pictograph_button, i // MAX_ITEMS_PER_ROW, i % MAX_ITEMS_PER_ROW
            )

    def on_pictograph_clicked(self) -> None:
        """
        Slot function called when a pictograph button is clicked.
        """
        pass

    def update_scroll_area_size(self) -> None:
        """
        Update the size of the scroll area based on the pictograph width and scrollbar width.
        """
        self.setFixedWidth(int(self.option_picker.width() * 4 / 5))
        self.setFixedHeight(int(self.option_picker.height()))
        self.pictograph_width = ((self.option_picker.width() * 5 / 6) / 4) - (
            self.verticalScrollBar().width() / 4
        )  - (self.spacing*2)
        self.pictograph_height = self.pictograph_width * (90 / 75)
        for button in self.grid_widget.findChildren(QPushButton):
            button.setFixedSize(int(self.pictograph_width), int(self.pictograph_height))
            button.setIconSize(
                QSize(int(self.pictograph_width), int(self.pictograph_height))
            )
