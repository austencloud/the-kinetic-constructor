from PyQt6.QtWidgets import QFrame
from widgets.graph_editor.infobox.infobox_buttons import InfoBoxButtons
from widgets.graph_editor.infobox.infobox_labels import InfoBoxLabels
from widgets.graph_editor.infobox.infobox_widgets import InfoBoxFrames
from widgets.graph_editor.infobox.infobox_layouts import InfoBoxLayouts
from widgets.graph_editor.graphboard.graphboard import GraphBoard
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class InfoBox(QFrame):
    def __init__(self, main_widget: "MainWidget", graphboard: "GraphBoard") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = self.main_widget.main_window
        self.graphboard = graphboard
        self.labels = InfoBoxLabels(self, graphboard)
        self.frames = InfoBoxFrames(self, graphboard)
        self.layouts = InfoBoxLayouts(self, graphboard)
        self.buttons = InfoBoxButtons(self, graphboard)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.buttons.setup_buttons()
        self.frames.setup_frames()
        self.layouts.setup_layouts()

    def update(self) -> None:
        self.frames.update_attribute_frames()
        if len(self.graphboard.staffs) == 2:
            self.labels.update_type_and_position_label()
