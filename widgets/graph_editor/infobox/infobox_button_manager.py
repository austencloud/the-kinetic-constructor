from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from objects.arrow.arrow import Arrow


class InfoboxButtonFactory:
    BUTTON_SIZE = 30

    def __init__(self, infobox, arrow_manipulator, graphboard_view):
        self.infobox = infobox
        self.arrow_manipulator = arrow_manipulator
        self.graphboard_view = graphboard_view

    def create_and_set_button(self, button_name, properties):
        """Create a button based on the provided properties and set it as a class attribute."""
        if properties["icon"]:
            button = QPushButton(QIcon(properties["icon"]), properties.get("text", ""))
        else:
            button = QPushButton(properties.get("text", ""))

        button.clicked.connect(properties["callback"])
        button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)

        setattr(self.infobox, f"{button_name}_button", button)
