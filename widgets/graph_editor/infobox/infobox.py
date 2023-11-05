from PyQt6.QtWidgets import QFrame
from widgets.graph_editor.infobox.infobox_buttons import InfoboxButtons
from widgets.graph_editor.infobox.infobox_labels import InfoboxLabels
from widgets.graph_editor.infobox.infobox_widgets import InfoboxWidgets
from widgets.graph_editor.infobox.infobox_layouts import InfoboxLayouts
from settings.numerical_constants import INFOBOX_SIZE
from settings.string_constants import RED, BLUE


class InfoboxFrame(QFrame):
    def __init__(
        self, main_widget, graphboard_view, arrow_manipulator, arrow_attributes
    ):
        super().__init__()
        self.main_widget = main_widget
        self.graphboard_view = graphboard_view
        self.arrow_manipulator = arrow_manipulator
        self.arrow_attributes = arrow_attributes
        self.setFixedSize(int(INFOBOX_SIZE), int(INFOBOX_SIZE))

    def init_manager(self):
        self.manager = InfoboxManager(
            self, self.arrow_manipulator, self.arrow_attributes, self.graphboard_view
        )

    def update(self):
        for color in [BLUE, RED]:
            arrows = self.graphboard_view.get_arrows_by_color(color)
            if arrows:
                attributes = self.arrow_attributes.create_dict_from_arrow(arrows[0])
                widget = getattr(self.manager.widgets, f"{color}_attributes_widget")
                self.manager.widgets.update_info_widget_content(widget, attributes)
                widget.setVisible(True)
            else:
                widget = getattr(self.manager.widgets, f"{color}_attributes_widget")
                widget.setVisible(False)


class InfoboxManager:
    def __init__(self, infobox, arrow_manipulator, arrow_attributes, graphboard_view):
        self.infobox = infobox
        self.graphboard_view = graphboard_view
        self.labels = InfoboxLabels(infobox, self, graphboard_view)
        self.widgets = InfoboxWidgets(infobox, self)
        self.layouts = InfoboxLayouts(infobox, self, graphboard_view, arrow_attributes)
        self.buttons = InfoboxButtons(infobox, self, arrow_manipulator, graphboard_view)
        self.setup_ui_elements()

    def setup_ui_elements(self):
        self.buttons.setup_buttons()
        self.labels.setup_labels()
        self.widgets.setup_widgets()
        self.layouts.setup_layouts()
