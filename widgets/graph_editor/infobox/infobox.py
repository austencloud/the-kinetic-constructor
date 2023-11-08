from PyQt6.QtWidgets import QFrame
from widgets.graph_editor.infobox.infobox_buttons import InfoboxButtons
from widgets.graph_editor.infobox.infobox_labels import InfoboxLabels
from widgets.graph_editor.infobox.infobox_widgets import InfoboxWidgets
from widgets.graph_editor.infobox.infobox_layouts import InfoboxLayouts
from settings.numerical_constants import INFOBOX_SIZE
from settings.string_constants import RED, BLUE


class Infobox(QFrame):
    def __init__(self, main_widget, graphboard, arrow_manipulator):
        super().__init__()
        self.main_widget = main_widget
        self.graphboard = graphboard
        self.arrow_manipulator = arrow_manipulator
        self.labels = InfoboxLabels(self, graphboard)
        self.widgets = InfoboxWidgets(self, graphboard)
        self.layouts = InfoboxLayouts(self, graphboard)
        self.buttons = InfoboxButtons(self, arrow_manipulator, graphboard)
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(int(INFOBOX_SIZE), int(INFOBOX_SIZE))
        self.buttons.setup_buttons()
        self.labels.setup_labels()
        self.widgets.setup_widgets()
        self.layouts.setup_layouts()

    def update(self):
        self.widgets.update_attribute_widgets()
        self.labels.update_type_and_position_label()


