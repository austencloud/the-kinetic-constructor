from widgets.graph_editor.infobox.infobox_button_factory import InfoboxButtonFactory
from widgets.graph_editor.infobox.infobox_helpers import InfoboxHelpers
from widgets.graph_editor.infobox.infobox_updater import InfoboxUpdater
from widgets.graph_editor.infobox.infobox_ui_setup import InfoboxUISetup

class InfoboxManager:
    def __init__(self, infobox):
        self.infobox = infobox
        self.helpers = InfoboxHelpers(infobox, self)
        self.updater = InfoboxUpdater(
            infobox, self, infobox.main_widget, infobox.graphboard_view
        )
        self.button_factory = InfoboxButtonFactory(
            infobox,
            infobox.graphboard_view.arrow_manager.manipulator,
            self.updater.graphboard_view,
        )
        self.ui_setup = InfoboxUISetup(infobox, self)


        self.finalize_ui_setup()

    def finalize_ui_setup(self):
        self.infobox.setLayout(self.ui_setup.master_layout)  