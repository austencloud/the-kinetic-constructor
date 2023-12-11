from typing import TYPE_CHECKING

from widgets.graph_editor.object_panel.objectbox_view import ObjectBoxView

if TYPE_CHECKING:
    from widgets.graph_editor.object_panel.arrowbox.arrowbox import ArrowBox
    from widgets.graph_editor.graph_editor import GraphEditor


class ArrowBoxView(ObjectBoxView):
    def __init__(self, arrowbox: "ArrowBox", graph_editor: "GraphEditor") -> None:
        super().__init__(arrowbox, graph_editor)
        self.setScene(arrowbox)
        self.arrowbox = arrowbox

    def leaveEvent(self, event) -> None:
        self.arrowbox.dim_all_arrows()
