from PyQt6.QtWidgets import QVBoxLayout
import logging
from widgets.graph_editor.infobox.infobox_button_manager import InfoboxButtonManager
from widgets.graph_editor.infobox.infobox_helpers import InfoboxHelpers
from widgets.graph_editor.infobox.infobox_updater import InfoboxUpdater
from widgets.graph_editor.infobox.infobox_setup import InfoboxSetup

class InfoboxManager:
    def __init__(self, infobox):
        self.infobox = infobox
        self.updater = InfoboxUpdater(self, self.infobox.main_widget, self.infobox.graphboard_view)
        self.button_manager = InfoboxButtonManager(self.infobox, self.updater.arrow_manipulator, self.updater.graphboard_view)
        self.helpers = InfoboxHelpers()
        self.updater = InfoboxUpdater(self, self.infobox.main_widget, self.infobox.graphboard_view)
        self.setup = InfoboxSetup(infobox, self)
        self.setup.setup_ui_elements()

    def update(self):
        self.updater.update_state()
        self.button_manager.update_buttons()
        self.updater.update_ui_elements()
