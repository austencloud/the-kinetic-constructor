from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from .splash_screen import SplashScreen


class SplashUpdater:
    """Manages progress updates for the splash screen."""

    def __init__(self, splash_screen: "SplashScreen"):
        self.splash_screen = splash_screen
        self.widget_messages = {
            "MenuBarWidget": "Initializing menu...",
            "NavigationWidget": "Setting up navigation...",
            "SequenceWidget": "Loading sequences...",
            "BuildTab": "Setting up build tab...",
            "BrowseTab": "Building dictionary...",
            "LearnTab": "Preparing lessons...",
            "WriteTab": "Setting up Act Tab...",
            "ManualBuilderWidget": "Loading manual builder...",
            "SequenceGeneratorWidget": "Setting up sequence generator...",
            "MainWidgetUI": "Configuring main UI...",
            "Finalizing": "Finalizing setup...",
        }
        self.current_progress = 0
        self.widget_progress_increment = 100 // len(self.widget_messages)

    def update_progress(self, widget_name: str):
        """Update the progress bar and message based on the widget being initialized."""
        # Increase progress and update the progress bar
        self.current_progress = min(
            100, self.current_progress + self.widget_progress_increment
        )
        self.splash_screen.progress_bar.setValue(self.current_progress)

        # Set the message based on the widget name
        message = self.widget_messages.get(widget_name, "Loading components...")
        self.splash_screen.currently_loading_label.setText(message)

        # Process events to immediately show updates
        QApplication.processEvents()
