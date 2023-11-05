from settings.numerical_constants import GRAPHBOARD_SCALE
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QSize

# ACTION BUTTONS #

ACTION_BUTTON_FONT = QFont("Helvetica", 14)
ACTION_BUTTON_SIZE = int(100 * GRAPHBOARD_SCALE)
ACTION_BUTTON_ICON_SIZE = QSize(int(80 * GRAPHBOARD_SCALE), int(70 * GRAPHBOARD_SCALE))
