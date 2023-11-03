from PyQt6.QtWidgets import QVBoxLayout
import logging
from widgets.graph_editor.infobox.infobox_button_manager import InfoboxButtonFactory
from widgets.graph_editor.infobox.infobox_helpers import InfoboxHelpers
from widgets.graph_editor.infobox.infobox_updater import InfoboxUpdater
from widgets.graph_editor.infobox.infobox_ui_setup import InfoboxUISetup
from widgets.graph_editor.infobox.infobox_controller import InfoboxController


class InfoboxManager:
    def __init__(self, infobox):
        self.updater = InfoboxUpdater(
            self, infobox.main_widget, infobox.graphboard_view
        )
        self.button_factory = InfoboxButtonFactory(
            infobox, self.updater.arrow_manipulator, self.updater.graphboard_view
        )
        self.helpers = InfoboxHelpers(self)
        self.setup = InfoboxUISetup(infobox, self)
        self.controller = InfoboxController(infobox, self)
