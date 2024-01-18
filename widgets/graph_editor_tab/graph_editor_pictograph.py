from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)
from objects.pictograph.pictograph import Pictograph
from widgets.graph_editor_tab.graph_editor_pictograph_view import (
    GraphEditorPictographView,
)

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.graph_editor_tab.graph_editor_frame import GraphEditorFrame


class GraphEditorPictograph(Pictograph):
    def __init__(
        self, main_widget: "MainWidget", graph_editor: "GraphEditorFrame"
    ) -> None:
        super().__init__(main_widget, graph_type="main")
        self.main_widget = main_widget
        self.graph_editor = graph_editor
        self.view: GraphEditorPictographView
