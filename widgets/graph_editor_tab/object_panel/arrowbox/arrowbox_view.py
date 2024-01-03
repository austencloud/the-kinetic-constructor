from typing import TYPE_CHECKING

from widgets.graph_editor_tab.object_panel.base_objectbox.base_objectbox_view import BaseObjectBoxView

if TYPE_CHECKING:
    from widgets.graph_editor_tab.object_panel.arrowbox.arrowbox import ArrowBox
    from widgets.graph_editor_tab.graph_editor_frame import GraphEditorFrame


class ArrowBoxView(BaseObjectBoxView):
    def __init__(self, arrowbox: "ArrowBox", graph_editor: "GraphEditorFrame") -> None:
        super().__init__(arrowbox, graph_editor)
        self.setScene(arrowbox)
        self.arrowbox = arrowbox

    def leaveEvent(self, event) -> None:
        self.arrowbox.dim_all_arrows()
