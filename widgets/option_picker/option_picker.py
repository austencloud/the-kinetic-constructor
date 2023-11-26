from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
from PyQt6.QtWidgets import QFrame, QHBoxLayout
from .letter_buttons import LetterButtons
from .scroll_area import ScrollArea


class OptionPicker(QFrame):
    """A class representing the OptionPicker widget.

    The OptionPicker widget provides a user interface for selecting options from a scrollable area.
    It consists of a scroll area and a frame containing buttons for each option.

    Attributes:
        main_widget (MainWidget): The main widget that contains the OptionPicker.
        main_window (QWidget): The main window of the application.
        main_layout (QHBoxLayout): The main layout of the OptionPicker widget.
        scroll_area (OptionPickerScrollArea): The scroll area widget for displaying options.
        button_frame (LetterButtons): The frame containing buttons for each option.

    """

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.main_layout = QHBoxLayout(self)
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface of the OptionPicker widget.

        This method initializes the layout and adds the scroll area and button frame to the main layout.

        """
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(self.width(), self.height())
        self.scroll_area = ScrollArea(self)
        self.button_frame = LetterButtons(self.main_widget, self)

        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.button_frame)

        self.setLayout(self.main_layout)

    ### RESIZE EVENT HANDLERS ###

    def update_size(self) -> None:
        """Update the size of the OptionPicker widget.

        This method is called when the size of the main widget changes.
        It updates the size of the OptionPicker widget based on the new size of the main widget.

        """
        self.setFixedSize(
            int(self.main_widget.width() * 0.5), int(self.main_widget.height() * 2 / 3)
        )

        self.scroll_area.update_scroll_area_size()
        self.button_frame.update_size()
