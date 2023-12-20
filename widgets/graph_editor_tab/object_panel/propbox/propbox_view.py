from typing import TYPE_CHECKING

from widgets.graph_editor_widget.object_panel.objectbox_view import ObjectBoxView

if TYPE_CHECKING:
    from widgets.graph_editor_widget.object_panel.propbox.propbox import PropBox
    from widgets.graph_editor_widget.graph_editor import GraphEditor


class PropBoxView(ObjectBoxView):
    def __init__(self, propbox: "PropBox", graph_editor: "GraphEditor") -> None:
        super().__init__(propbox, graph_editor)
        self.setScene(propbox)
        self.propbox = propbox
