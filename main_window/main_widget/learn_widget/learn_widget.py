from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QResizeEvent

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class LearnWidget(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.background_manager = None
        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )
        self.initialized = False
        self.buttons: dict[str, QPushButton] = {}
        # Initial layout with module selection
        self._setup_layout()

        # Initialize background manager and connect signals
        self.connect_background_manager()

        # Initialize the module selection screen
        self.init_module_selection_screen()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

    def connect_background_manager(self):
        """Connect to the background manager to maintain consistent backgrounds."""
        self.main_widget.main_window.settings_manager.background_changed.connect(
            self.update_background_manager
        )

    def update_background_manager(self, bg_type: str):
        self.background_manager = self.global_settings.setup_background_manager(self)
        self.background_manager.update_required.connect(self.update)
        self.update()

    def init_module_selection_screen(self):
        """Creates the initial screen with module selections."""
        # Create title label
        title_label = QLabel("Select Difficulty")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addStretch(2)
        self.layout.addWidget(title_label)

        # Add vertical space before buttons
        self.layout.addStretch(2)

        # Create buttons for each module
        self.button_layout = QVBoxLayout()

        # Add buttons with module names and callbacks
        self.add_module_button("Basic", self.start_basic_module)
        self.add_module_button("Intermediate", self.start_intermediate_module)
        self.add_module_button("Advanced", self.start_advanced_module)

        # Add vertical space after buttons

        self.layout.addLayout(self.button_layout)
        self.layout.addStretch(3)

    def add_module_button(self, text: str, callback):
        """Helper method to add a module button with dynamic sizing."""
        button = QPushButton(text)
        button.clicked.connect(callback)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.buttons[text] = button
        # Set size policy to expand dynamically with widget size
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Add the button to the layout
        self.button_layout.addWidget(button)

    def start_basic_module(self):
        """Start the basic module."""
        print("Starting Basic Module")

    def start_intermediate_module(self):
        """Start the intermediate module."""
        print("Starting Intermediate Module")

    def start_advanced_module(self):
        """Start the advanced module."""
        print("Starting Advanced Module")

    def resize_learn_widget(self) -> None:
        """Dynamically adjust button sizes and font sizes based on window size."""
        # Set button width to 1/5th of the widget's width
        for button in self.buttons.values():
            button.setFixedWidth(self.main_widget.width() // 5)
            button.setFixedHeight(self.main_widget.height() // 5)
            # make the button text bigger
            font = button.font()
            font.setPointSize(self.main_widget.height() // 50)
            button.setFont(font)
            
    def paintEvent(self, event):
        """Draw the background using the background manager."""
        if self.background_manager is None:
            self.background_manager = self.global_settings.setup_background_manager(
                self
            )
        painter = QPainter(self)
        self.background_manager.paint_background(self, painter)
