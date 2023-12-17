
from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
)
from objects.pictograph.pictograph import Pictograph
from widgets.sequence_widget.beat_frame.beat_frame import BeatFrame

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class Beat(Pictograph):
    def __init__(self, main_widget: "MainWidget", Sequence: "BeatFrame") -> None:
        super().__init__(main_widget, main_widget.graph_editor_widget.graph_editor)
        self.main_widget = main_widget
        self.sequence = Sequence

        self.setup_scene()
        self.setup_components(main_widget)
