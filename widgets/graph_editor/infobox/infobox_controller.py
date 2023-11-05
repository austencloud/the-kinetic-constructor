from PyQt6.QtWidgets import QVBoxLayout

class InfoboxController:
    def __init__(self, infobox, infobox_manager):
        self.infobox = infobox
        self.graphboard_view = infobox.graphboard_view
        self.infobox_manager = infobox_manager
        self.updater = infobox_manager.updater
        self.button_factory = infobox_manager.button_factory
        self.arrow_manipulator = self.infobox.graphboard_view.arrow_manager.manipulator
