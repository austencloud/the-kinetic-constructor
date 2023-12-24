from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)
from objects.pictograph.pictograph import Pictograph
from widgets.graph_editor_tab.main_pictograph_view import MainPictographView

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor_tab.graph_editor import GraphEditor


class MainPictograph(Pictograph):
    def __init__(self, main_widget: "MainWidget", graph_editor: "GraphEditor") -> None:
        super().__init__(main_widget, graph_type="main")
        self.main_widget = main_widget
        self.graph_editor = graph_editor
        self.view: MainPictographView