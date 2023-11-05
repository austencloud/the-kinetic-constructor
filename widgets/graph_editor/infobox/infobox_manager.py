
from widgets.graph_editor.infobox.infobox_helpers import InfoboxHelpers
from widgets.graph_editor.infobox.infobox_updater import InfoboxUpdater
from widgets.graph_editor.infobox.infobox_ui_setup import InfoboxUISetup
from widgets.graph_editor.infobox.infobox_buttons import InfoboxButtons
from widgets.graph_editor.infobox.infobox_labels import InfoboxLabels
from widgets.graph_editor.infobox.infobox_widgets import InfoboxWidgets
from widgets.graph_editor.infobox.infobox_layouts import InfoboxLayouts

class InfoboxManager:
    def __init__(self, infobox):
        self.infobox = infobox
        self.labels = InfoboxLabels(infobox, self)
        self.widgets = InfoboxWidgets(self)
        self.layouts = InfoboxLayouts(infobox, infobox.graphboard_view)
        self.helpers = InfoboxHelpers(infobox, self)
        self.updater = InfoboxUpdater(
            infobox, self, infobox.main_widget, infobox.graphboard_view
        )
        self.buttons = InfoboxButtons(
            infobox,
            infobox.graphboard_view.arrow_manager.manipulator,
            self.updater.graphboard_view,
        )
        self.ui_setup = InfoboxUISetup(infobox, self)

        self.finalize_ui_setup()

    def finalize_ui_setup(self):
        self.infobox.setLayout(self.ui_setup.master_layout)
