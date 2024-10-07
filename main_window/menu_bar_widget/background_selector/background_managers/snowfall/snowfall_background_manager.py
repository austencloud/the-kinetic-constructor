import random
from typing import TYPE_CHECKING, Union
from main_window.menu_bar_widget.background_selector.background_managers.background_manager import (
    BackgroundManager,
)
from PyQt6.QtGui import QColor, QPainter, QLinearGradient
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_widget import (
        DictionaryWidget,
    )
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget
    from main_window.main_widget.top_builder_widget.top_builder_widget import (
        TopBuilderWidget,
    )


from .snowflake_manager import SnowflakeManager
from .santa_manager import SantaManager
from .shooting_star_manager import ShootingStarManager  # Import the new manager

class SnowfallBackgroundManager(BackgroundManager):
    def __init__(self, widget: Union["TopBuilderWidget", "DictionaryWidget", "LearnWidget"]):
        super().__init__(widget)
        self.widget = widget

        # Initialize managers
        self.snowflake_manager = SnowflakeManager()
        self.santa_manager = SantaManager()
        self.shooting_star_manager = ShootingStarManager()  # Add shooting star manager

    def animate_background(self):
        # Delegate animation to managers
        self.snowflake_manager.animate_snowflakes()
        self.santa_manager.animate_santa()
        self.shooting_star_manager.animate_shooting_star()  # Animate shooting stars
        self.shooting_star_manager.manage_shooting_star(self.widget)  # Manage shooting star timing
        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw the gradient background
        gradient = QLinearGradient(0, 0, 0, widget.height())
        gradient.setColorAt(0, QColor(20, 30, 48))  # Dark blue at top
        gradient.setColorAt(1, QColor(50, 80, 120))  # Slightly lighter blue at bottom
        painter.fillRect(widget.rect(), gradient)

        # Delegate drawing to managers
        self.snowflake_manager.draw_snowflakes(painter, widget)
        if self.santa_manager.santa["active"]:
            self.santa_manager.draw_santa(painter, widget)

        # Draw the shooting star if it's active
        self.shooting_star_manager.draw_shooting_star(painter, widget)
