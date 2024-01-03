from typing import TYPE_CHECKING

from widgets.graph_editor_tab.graph_editor_object_panel.base_objectbox.base_objectbox_view import (
    BaseObjectBoxView,
)


if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_object_panel.propbox.propbox import (
        PropBox,
    )
    from widgets.graph_editor_tab.graph_editor_frame import GraphEditorFrame


class PropBoxView(BaseObjectBoxView):
    def __init__(self, propbox: "PropBox", graph_editor: "GraphEditorFrame") -> None:
        super().__init__(propbox, graph_editor)
        self.setScene(propbox)
        self.propbox = propbox
