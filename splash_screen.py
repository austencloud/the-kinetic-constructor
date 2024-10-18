from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtGui import QPixmap, QFont, QFontMetrics, QScreen, QPainter
from PyQt6.QtCore import Qt

from main_window.main_widget.dictionary_widget.dictionary_browser.rainbow_progress_bar import (
    RainbowProgressBar,
)
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_window import MainWindow
    from main_window.settings_manager.settings_manager import SettingsManager


class SplashScreen(QWidget):
    def __init__(self, target_screen: QScreen, settings_manager: "SettingsManager"):
        super().__init__()
        self.target_screen = target_screen
        self.settings_manager = settings_manager

        self._setup_window_properties()
        self._create_components()
        self.main_widget = None
        self.background_manager = (
            self.settings_manager.global_settings.setup_background_manager(
                self, is_splash_screen=True
            )
        )
        self._setup_layout()
        self._center_on_screen()
        self.show()

    def _setup_window_properties(self):
        """Set window flags, background, and size."""
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

        screen_geometry = self.target_screen.geometry()
        self.splash_screen_width = int(screen_geometry.width() // 2.5)
        self.splash_screen_height = int(screen_geometry.height() // 2.5)
        self.setFixedSize(self.splash_screen_width, self.splash_screen_height)

    def _create_components(self):
        """Create the components used in the splash screen."""

        self.title_label = self._create_title_label()
        self.currently_loading_label = self._create_label("Importing modules...")
        self.created_by_label = QLabel("Created by Austen Cloud")
        self.created_by_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        created_by_font = QFont("Cambria", self.splash_screen_height // 40)
        created_by_font.setBold(True)
        self.created_by_label.setFont(created_by_font)

        # set created by label to bold
        created_by_font = self.created_by_label.font()
        created_by_font.setBold(True)

        self.progress_bar = RainbowProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        progress_bar_font = self.progress_bar.percentage_label.font()
        progress_bar_font.setFamily("Monotype Corsiva")  # Set font to Monotype Corsiva
        progress_bar_font.setPointSize(self.width() // 40)
        self.progress_bar.percentage_label.setFont(progress_bar_font)
        self.progress_bar.loading_label.hide()

        # Logo (image) setup
        self.logo_label = self._setup_logo()

    def _setup_layout(self):
        """Set up the layout, adding components to the appropriate positions."""
        layout = QVBoxLayout(self)

        # Create the top layout (for text and logo)
        top_layout, bottom_layout = self._create_layouts()

        # Left side (progress and text)
        left_layout = QVBoxLayout()
        left_layout.addStretch(1)
        left_layout.addWidget(self.title_label)
        left_layout.addStretch(1)
        left_layout.addWidget(self.created_by_label)
        left_layout.addStretch(1)
        left_layout.addWidget(self.currently_loading_label)
        left_layout.addStretch(1)

        top_layout.addLayout(left_layout)

        # Right side (image/logo)
        top_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignRight)

        # Add the top layout to the main layout
        layout.addLayout(top_layout)

        # Add a QSpacerItem to push the progress bar to the bottom
        spacer_height = self.height() // 10
        layout.addSpacerItem(
            QSpacerItem(
                20,
                spacer_height,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Expanding,
            )
        )

        # Add the progress bar at the bottom
        bottom_layout.addWidget(self.progress_bar)

        # Add the bottom layout (progress bar) to the main layout
        layout.addLayout(bottom_layout)

    def _create_layouts(self):
        """Create the top and bottom layouts."""
        top_layout = QHBoxLayout()  # For left (text/progress) and right (logo)
        bottom_layout = QHBoxLayout()  # For the progress bar
        return top_layout, bottom_layout

    def _create_title_label(self) -> QLabel:
        """Create the title label with Monotype Corsiva and manage its font size."""
        title_font = QFont("Monotype Corsiva", self.splash_screen_height // 10)
        title_label = QLabel("The\nKinetic\nConstructor")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(title_font)

        # Ensure title does not exceed allotted space using font metrics
        font_metrics = QFontMetrics(title_font)
        if font_metrics.horizontalAdvance(title_label.text()) > (
            self.splash_screen_width // 2
        ):
            title_font.setPointSize(title_font.pointSize() - 2)
            title_label.setFont(title_font)

        return title_label

    def _create_label(self, text: str) -> QLabel:
        """Helper to create a generic label."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Arial", self.splash_screen_height // 40))
        return label

    def _setup_logo(self) -> QLabel:
        """Set up the right-side logo image with square dimensions."""
        # Load the image
        splash_pix = QPixmap(get_images_and_data_path("images/splash_screen.png"))

        # Get the available width and height for the logo
        available_width = self.splash_screen_width // 2
        available_height = self.splash_screen_height

        # Scale the pixmap to fit within the available height while keeping aspect ratio
        scaled_splash_pix = splash_pix.scaled(
            available_width,
            available_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # Create QLabel for the image
        logo_label = QLabel()
        logo_label.setPixmap(scaled_splash_pix)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setMaximumSize(available_width, available_height)
        return logo_label

    def _center_on_screen(self):
        """Center the splash screen on the target screen."""
        screen_geometry = self.target_screen.geometry()
        self.setGeometry(
            screen_geometry.x() + (screen_geometry.width() - self.width()) // 2,
            screen_geometry.y() + (screen_geometry.height() - self.height()) // 2,
            self.width(),
            self.height(),
        )

    def paintEvent(self, event):
        """Handle painting the custom background using the background manager."""
        painter = QPainter(self)
        self.background_manager.paint_background(self, painter)
        # super().paintEvent(event)

    def update_progress(self, value, message=""):
        """Update progress bar and message."""
        self.progress_bar.setValue(value)
        if message:
            self.currently_loading_label.setText(message)

    def finish(self):
        """Close the splash screen and show the main window."""
        self.close()
